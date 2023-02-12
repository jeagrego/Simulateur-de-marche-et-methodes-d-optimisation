import DisplayModel
import Model
import Animal
import sys


if __name__ == "__main__":
    model = Model.Model(4, 100, 200, 100)
    """Animal.Cow(4, 100, 150, 332.75, 200, 100)"""
    display = DisplayModel.Display(model)
    sys.exit(display.show())
    """vache = Model.Vache(4, 600)
    autruche = Model.Autruche(2, 120)

    print(autruche.getPattes())
    print(vache.getPattes())
    vache.setScore(100)
    print(vache.getScore())"""