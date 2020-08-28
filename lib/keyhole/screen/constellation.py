import random


class Constellation():
    def __init__(self):
        self.constellation = [
            [
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "      o                                 ",
                "            *                           ",
                "                                        ",
                "                                        ",
                "                .                       ",
                "                                        ",
                "                                        ",
                "                    *                   ",
                "                                        ",
                "                                        ",
                "                             o          ",
                "                    o                   ",
                "                                        ",
                "                          .             ",
                "                                        ",
                "                                        ",
            ],
            [
                "              .                         ",
                "                                        ",
                "                    o                   ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "          o                             ",
                "                                        ",
                "                                        ",
                "                      *                 ",
                "                                        ",
                "                     *                  ",
                "                                        ",
                "                    *                   ",
                "                        .               ",
                "                         .              ",
                "                          .     *       ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                      o                 ",
            ],
            [
                "                   .                    ",
                "               *                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "               .                        ",
                "                                        ",
                "                      o                 ",
                "                 o                      ",
                "                          o             ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "                                        ",
                "           .                            ",
                "                                        ",
                "                                        ",
                "              .                         ",
                "                                        ",
                "                                        ",
                "          *                             ",
            ],
        ]

    def get_rand(self):
        return random.choice(self.constellation)