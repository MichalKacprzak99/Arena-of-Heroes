class Hero:
    def __init__(self, image_id, hero_id, pos, which_side="east", name="HERO"):
        self.image_id = image_id
        self.hero_id = hero_id
        self.pos = pos
        self.health = 75
        self.range = 5
        self.which_side = which_side
        self.name = name

