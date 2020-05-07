class Hero:
    def __init__(self, image_id, hero_id, pos, which_side="east", name="HERO"):
        self.image_id = image_id
        self.hero_id = hero_id
        self.pos = pos
        self.which_side = which_side
        self.hp = 100
        self.attributes = {
            "NAME": name,
            "MAX HP": 100,
            "HP": self.hp,
            "ATTACK": 10,
            "DEFENSE": 10,
            "RANGE": 5
        }
