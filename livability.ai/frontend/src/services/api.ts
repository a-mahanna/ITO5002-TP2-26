const API_BASE_URL = 'https://ito5002-tp2-26.onrender.com'

export interface SuburbApiResponse {
  name?: string | null
  suburb?: string | null
  info?: string | null
  description?: string | null
  median_rent?: number | null
  affordability_score?: number | null
  safety_score?: number | null
  transport_score?: number | null
  crime_rate?: number | null
  pt_score?: number | null
  distance_to_cbd_km?: number | null
  rent?: {
    ['1bed_flat']?: number | null
    ['2bed_flat']?: number | null
    ['3bed_flat']?: number | null
    ['2bed_house']?: number | null
    ['3bed_house']?: number | null
    ['4bed_house']?: number | null
  }
  crime?: {
    total_offences?: number | null
  }
  transport?: {
    bus_stops?: number | null
    train_stops?: number | null
    tram_stops?: number | null
    total_stops?: number | null
    weighted_score?: number | null
  }
  scores?: {
    rent_score?: number | null
    safety_score?: number | null
    transport_score?: number | null
  }
  [key: string]: unknown
}

export interface AveragesApiResponse {
  median_rent?: number | null
  affordability_score?: number | null
  safety_score?: number | null
  transport_score?: number | null
  crime_rate?: number | null
  pt_score?: number | null
  [key: string]: unknown
}

export interface RecommendResult {
  suburb: string
  preference_score: number
  rent: number | null
  scores?: {
    rent_score?: number | null
    safety_score?: number | null
    transport_score?: number | null
  }
  transport?: {
    bus_stops?: number | null
    train_stops?: number | null
    tram_stops?: number | null
    total_stops?: number | null
    weighted_score?: number | null
  }
  crime?: {
    total_offences?: number | null
  }
  explanation?: string | null
  distance_to_cbd_km?: number | null
}

export interface RecommendApiResponse {
  budget: number
  property_type: string
  weights: {
    safety: number
    transport: number
  }
  count: number
  message?: string
  recommendations: RecommendResult[]
}

export async function fetchRecommendations(params: {
  budget: number
  propertyType: string
  safetyWeight: number
  transportWeight: number
  n?: number
}): Promise<RecommendApiResponse> {
  const query = new URLSearchParams({
    budget: String(params.budget),
    property_type: params.propertyType,
    safety_weight: String(params.safetyWeight),
    transport_weight: String(params.transportWeight),
    n: String(params.n ?? 10),
  })

  const url = `${API_BASE_URL}/api/v2/recommend?${query.toString()}`
  console.log('Fetching recommendations from:', url)

  let response: Response

  try {
    response = await fetch(url)
  } catch (err) {
    throw new Error(`Network error while fetching recommendations from ${url}`)
  }

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to fetch recommendations: ${response.status} ${text}`)
  }

  return response.json()
}

function normaliseName(name: string) {
  return name.trim()
}

function firstRentValue(rent?: SuburbApiResponse['rent']): number | null {
  if (!rent) return null

  return (
    rent['2bed_house'] ??
    rent['2bed_flat'] ??
    rent['3bed_house'] ??
    rent['1bed_flat'] ??
    rent['3bed_flat'] ??
    rent['4bed_house'] ??
    null
  )
}

function normaliseSuburbResponse(raw: any): SuburbApiResponse {
  const suburb = raw?.suburb ?? raw

  return {
    ...suburb,
    name: suburb?.name ?? null,
    suburb: suburb?.name ?? null,
    info: suburb?.info ?? suburb?.description ?? null,
    description: suburb?.description ?? null,
    median_rent: suburb?.median_rent ?? firstRentValue(suburb?.rent),
    affordability_score:
      suburb?.affordability_score ?? suburb?.scores?.rent_score ?? null,
    safety_score:
      suburb?.safety_score ?? suburb?.scores?.safety_score ?? null,
    transport_score:
      suburb?.transport_score ?? suburb?.scores?.transport_score ?? null,
    crime_rate:
      suburb?.crime_rate ?? suburb?.crime?.total_offences ?? null,
    pt_score:
      suburb?.pt_score ?? suburb?.transport?.weighted_score ?? null,
    distance_to_cbd_km: suburb?.distance_to_cbd_km ?? null,
    rent: suburb?.rent ?? undefined,
    crime: suburb?.crime ?? undefined,
    transport: suburb?.transport ?? undefined,
    scores: suburb?.scores ?? undefined,
  }
}

function normaliseAveragesResponse(raw: any): AveragesApiResponse {
  const avg = raw?.melbourne_averages ?? raw

  return {
    median_rent:
      avg?.median_rent ??
      avg?.median_rent_2bed_house ??
      avg?.median_rent_2bed_flat ??
      avg?.median_rent_3bed_house ??
      avg?.median_rent_1bed_flat ??
      null,
    affordability_score: avg?.affordability_score ?? null,
    safety_score: avg?.safety_score ?? null,
    transport_score:
      avg?.transport_score ??
      avg?.weighted_transport_score ??
      null,
    crime_rate: avg?.crime_rate ?? avg?.total_offences ?? null,
    pt_score: avg?.pt_score ?? avg?.weighted_transport_score ?? null,
  }
}

export async function fetchSuburbByName(name: string): Promise<SuburbApiResponse> {
  const cleaned = normaliseName(name)
  const response = await fetch(
    `${API_BASE_URL}/api/v1/suburbs/${encodeURIComponent(cleaned)}`
  )

  if (!response.ok) {
    throw new Error(`Failed to fetch suburb details for "${cleaned}"`)
  }

  const raw = await response.json()
  return normaliseSuburbResponse(raw)
}

export async function fetchAllSuburbs(): Promise<SuburbApiResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/suburbs/all`)

  if (!response.ok) {
    throw new Error('Failed to fetch all suburbs')
  }

  const raw = await response.json()

  if (Array.isArray(raw)) {
    return raw.map(normaliseSuburbResponse)
  }

  if (Array.isArray(raw?.suburbs)) {
    return raw.suburbs.map(normaliseSuburbResponse)
  }

  return []
}

export async function fetchAverages(): Promise<AveragesApiResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/averages`)

  if (!response.ok) {
    throw new Error('Failed to fetch Melbourne averages')
  }

  const raw = await response.json()
  return normaliseAveragesResponse(raw)
}

export async function searchSuburbs(query: string): Promise<any> {
  const cleaned = query.trim()
  const response = await fetch(
    `${API_BASE_URL}/api/v1/search?q=${encodeURIComponent(cleaned)}`
  )

  if (!response.ok) {
    throw new Error(`Failed to search suburbs for "${cleaned}"`)
  }

  return response.json()
}
