class SuburbRecommender:
    def recommend(self, budget, property_type="2bed_flat", safety_weight=0.5,
                transport_weight=0.5, n=10):
        """Rank suburbs by user preferences."""
        rent_key = property_type

        candidates = []
        for s in self.suburbs_list:
            rent = s.get("rent", {}).get(rent_key)
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

        total = safety_weight + transport_weight
        w_safety = safety_weight / total if total > 0 else 0.5
        w_transport = transport_weight / total if total > 0 else 0.5

        scored = []
        for s in candidates:
            safety = s.get("scores", {}).get("safety_score")
            transport = s.get("scores", {}).get("transport_score")

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
                "suburb": s.get("name"),
                "preference_score": float(pref_score),
                "rent": s.get("rent", {}).get(rent_key),
                "scores": s.get("scores", {}),
                "transport": s.get("transport", {}),
                "crime": s.get("crime", {}),
                "explanation": explanation["explanation"] if explanation else None,
                "distance_to_cbd_km": s.get("distance_to_cbd_km"),
            })

        scored.sort(key=lambda x: x["preference_score"], reverse=True)

        return {
            "budget": budget,
            "property_type": property_type,
            "weights": {
                "safety": round(w_safety, 2),
                "transport": round(w_transport, 2)
            },
            "count": len(scored),
            "recommendations": scored[:n]
        }