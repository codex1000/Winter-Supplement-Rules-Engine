class WinterSupplementRulesEngine:
    @staticmethod
    def calculate_supplement(data):
        base_amount = 0.0
        children_amount = 0.0

        if not data.get("familyUnitInPayForDecember", False):
            return {
                "id": data["id"],
                "isEligible": False,
                "baseAmount": 0.0,
                "childrenAmount": 0.0,
                "supplementAmount": 0.0,
            }

        family_composition = data.get("familyComposition", "single")
        if family_composition == "single":
            base_amount = 60.0
        elif family_composition == "couple":
            base_amount = 120.0

        number_of_children = data.get("numberOfChildren", 0)
        children_amount = 20.0 * number_of_children

        supplement_amount = base_amount + children_amount

        return {
            "id": data["id"],
            "isEligible": True,
            "baseAmount": base_amount,
            "childrenAmount": children_amount,
            "supplementAmount": supplement_amount,
        }