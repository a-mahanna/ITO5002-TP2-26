"""
recommender.py — Livability.AI AI Engine
V2 Features: Explainability, Similarity, Clustering
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


class SuburbRecommender:
    def __init__(self, suburbs_data):
        """Initialise with suburb data from suburbs.json."""
        self.suburbs = {s["name"].lower(): s for s in suburbs_data}
        self.suburbs_list = suburbs_data
        self._build_feature_matrix()
        self._build_clusters()

    def _build_feature_matrix(self):
        """Build normalised feature vectors for similarity calculations."""
        self.feature_names = []
        features = []

        for s in self.suburbs_list:
            rent = s["scores"].get("rent_score")
            safety = s["scores"].get("safety_score")
            transport = s["scores"].get("transport_score")

            # Only include suburbs with at least rent + safety
            if rent is not None and safety is not None:
                self.feature_names.append(s["name"])
                features.append([
                    rent,
                    safety,
                    transport if transport is not None else 50.0
                ])

        if features:
            self.feature_matrix = np.array(features)
            self.similarity_matrix = cosine_similarity(self.feature_matrix)
        else:
            self.feature_matrix = np.array([])
            self.similarity_matrix = np.array([])

        print(f"  Recommender: {len(self.feature_names)} suburbs with feature vectors")

    def _build_clusters(self, n_clusters=5):
        """K-means clustering of suburbs by metric profiles."""
        if len(self.feature_matrix) < n_clusters:
            self.cluster_labels = []
            self.clusters = {}
            return

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_labels = kmeans.fit_predict(self.feature_matrix)

        self.clusters = {}
        for i in range(n_clusters):
            mask = self.cluster_labels == i
            cluster_features = self.feature_matrix[mask]
            cluster_suburbs = [self.feature_names[j]
                               for j in range(len(self.feature_names)) if mask[j]]

            self.clusters[i] = {
                "cluster_id": i,
                "suburb_count": len(cluster_suburbs),
                "suburbs": cluster_suburbs,
                "avg_rent_score": round(float(cluster_features[:, 0].mean()), 1),
                "avg_safety_score": round(float(cluster_features[:, 1].mean()), 1),
                "avg_transport_score": round(float(cluster_features[:, 2].mean()), 1),
            }

        print(f"  Clusters: {n_clusters} groups created")

    # =============================================
    # FEATURE 1: EXPLAINABILITY
    # =============================================
    def explain(self, suburb_name, budget=None):
        """Generate plain-English explanation for a suburb."""
        key = suburb_name.lower()
        if key not in self.suburbs:
            return None

        s = self.suburbs[key]
        name = s["name"]
        parts = []

        # Rent
        rent_2bed = s["rent"].get("2bed_flat")
        if rent_2bed is not None:
            text = f"The median rent for a 2-bedroom flat is ${int(rent_2bed)}/week"
            if budget is not None:
                if rent_2bed <= budget:
                    diff = round(((budget - rent_2bed) / budget) * 100)
                    text += f", which is {diff}% below your budget of ${int(budget)}"
                else:
                    text += f", which exceeds your budget of ${int(budget)}"
            parts.append(text)

        # Crime
        offences = s["crime"].get("total_offences")
        if offences is not None:
            all_offences = [sub["crime"]["total_offences"]
                           for sub in self.suburbs_list
                           if sub["crime"].get("total_offences") is not None]
            if all_offences:
                avg = round(np.mean(all_offences))
                if offences < avg:
                    diff_pct = round(((avg - offences) / avg) * 100)
                    parts.append(f"Total recorded offences ({offences}) are {diff_pct}% below the Melbourne average ({avg})")
                else:
                    diff_pct = round(((offences - avg) / avg) * 100)
                    parts.append(f"Total recorded offences ({offences}) are {diff_pct}% above the Melbourne average ({avg})")

        # Transport
        t = s["transport"]
        transport_parts = []
        if t.get("train_stops", 0) > 0:
            n = t["train_stops"]
            transport_parts.append(f"{n} train stop{'s' if n != 1 else ''}")
        if t.get("tram_stops", 0) > 0:
            n = t["tram_stops"]
            transport_parts.append(f"{n} tram stop{'s' if n != 1 else ''}")
        if t.get("bus_stops", 0) > 0:
            n = t["bus_stops"]
            transport_parts.append(f"{n} bus stop{'s' if n != 1 else ''}")
        if transport_parts:
            parts.append(f"Public transport includes {', '.join(transport_parts)}")

        explanation = f"{name} — " + ". ".join(parts) + "." if parts else f"{name} — insufficient data for explanation."

        return {
            "suburb": name,
            "explanation": explanation,
            "metrics": s,
            "budget": budget,
            "within_budget": rent_2bed <= budget if (rent_2bed and budget) else None
        }

    # =============================================
    # FEATURE 2: SIMILARITY
    # =============================================
    def find_similar(self, suburb_name, n=5):
        """Find most similar suburbs using cosine similarity."""
        key = suburb_name.lower()
        if key not in self.suburbs:
            return None

        name = self.suburbs[key]["name"]

        try:
            idx = [s.lower() for s in self.feature_names].index(key)
        except ValueError:
            return {"suburb": name, "error": "Insufficient data for similarity", "similar": []}

        similarities = self.similarity_matrix[idx]
        similar_indices = np.argsort(similarities)[::-1]
        similar_indices = [i for i in similar_indices if i != idx][:n]

        results = []
        for i in similar_indices:
            sim_name = self.feature_names[i]
            sim_data = self.suburbs[sim_name.lower()]
            results.append({
                "suburb": sim_name,
                "similarity_score": round(float(similarities[i]), 3),
                "rent": sim_data["rent"],
                "crime": sim_data["crime"],
                "transport": sim_data["transport"],
                "scores": sim_data["scores"],
            })

        # Cluster context
        cluster_info = None
        if hasattr(self, "cluster_labels") and len(self.cluster_labels) > 0:
            cluster_id = int(self.cluster_labels[idx])
            cluster = self.clusters.get(cluster_id, {})
            cluster_info = {
                "cluster_id": cluster_id,
                "suburbs_in_cluster": cluster.get("suburb_count", 0),
                "avg_rent_score": cluster.get("avg_rent_score"),
                "avg_safety_score": cluster.get("avg_safety_score"),
                "avg_transport_score": cluster.get("avg_transport_score"),
            }

        return {
            "suburb": name,
            "similar": results,
            "cluster": cluster_info
        }

    # =============================================
    # RECOMMENDER: MATCH PREFERENCES
    # =============================================
    def recommend(self, budget, property_type="2bed_flat", safety_weight=0.5,
                  transport_weight=0.5, n=10):
        """Rank suburbs by user preferences."""
        rent_key = property_type

        candidates = []
        for s in self.suburbs_list:
            rent = s["rent"].get(rent_key)
            if rent is not None and rent <= budget:
                candidates.append(s)

        if not candidates:
            return {
                "budget": budget,
                "property_type": property_type,
                "count": 0,
                "message": f"No suburbs found with {property_type} under ${budget}/week",
                "recommendations": []
            }

        # Normalise weights
        total = safety_weight + transport_weight
        w_safety = safety_weight / total if total > 0 else 0.5
        w_transport = transport_weight / total if total > 0 else 0.5

        scored = []
        for s in candidates:
            safety = s["scores"].get("safety_score")
            transport = s["scores"].get("transport_score")

            if safety is None:
                safety = 50
            if transport is None:
                transport = 50

            pref_score = round((w_safety * safety) + (w_transport * transport), 1)

            explanation = None
            try:
                explanation = self.explain(s["name"], budget)
            except Exception:
                explanation = None

            scored.append({
                "suburb": s["name"],
                "preference_score": pref_score,
                "rent": s["rent"].get(rent_key),
                "scores": s["scores"],
                "transport": s["transport"],
                "crime": s["crime"],
                "explanation": explanation["explanation"] if explanation else None,
                "distance_to_cbd_km": s.get("distance_to_cbd_km"),
            })

        scored.sort(key=lambda x: x["preference_score"], reverse=True)

        return {
            "budget": budget,
            "property_type": property_type,
            "weights": {"safety": round(w_safety, 2), "transport": round(w_transport, 2)},
            "count": len(scored),
            "recommendations": scored[:n]
        }

    # =============================================
    # CLUSTERS
    # =============================================
    def get_clusters(self):
        """Return cluster summaries."""
        if not self.clusters:
            return {"error": "Clusters not computed", "clusters": []}
        return {
            "cluster_count": len(self.clusters),
            "clusters": list(self.clusters.values())
        }