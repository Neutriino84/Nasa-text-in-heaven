from vpython import *
from random import uniform

scene.title = "NASA 3D"
scene.background = color.black

# -------------------
# Asetetaan koko näytön koko ja kamera
# -------------------
scene.width = 1920          # voit laittaa haluamasi leveyden
scene.height = 1080         # korkeus
scene.autoscale = True
scene.center = vector(0,0,0)
scene.camera.pos = vector(0,0,10)   # kameran paikka
scene.camera.axis = vector(0,0,-10) # mihin kamera katsoo


# Valo
distant_light(direction=vector(1,1,1), color=color.white)

# 3D teksti
nasa = text(
    text="NASA",
    align="center",
    height=2,
    depth=0.5,      # tekee siitä 3D
    color=color.white
)

stars = []

for i in range(200):
    star = sphere(
        pos=vector(
            uniform(-10,10),
            uniform(-5,5),
            uniform(-20,-2)
        ),
        radius=0.05,
        color=color.white,
        emissive=True
    )
    stars.append(star)

# -------------------
# 3D-avaruusalus (kuuraketti)
# -------------------

# -------------------
# Rakettien tiedot
# -------------------
rocket_count = 4
rockets = []

for i in range(rocket_count):
    # Aloituspaikka satunnaisesti x- ja y-suunnassa
    start_pos = vector(-2 - i*1.5, uniform(-1,1), -5)
    
    # Runko
    body = cylinder(pos=start_pos, axis=vector(2,1,0), radius=0.2, color=color.red)
    # Keula
    nose = cone(pos=body.pos + body.axis, axis=vector(0.5,0.25,0), radius=0.2, color=color.orange)
    # Siivet
    wing_top = pyramid(pos=body.pos + vector(0.5,0.6,0), size=vector(0.5,0.05,0.4), color=color.gray(0.5))
    wing_bottom = pyramid(pos=body.pos + vector(0.5,-0.6,0), size=vector(0.5,0.05,0.4), color=color.gray(0.5))
    # Lieska perässä
    flame = cone(pos=body.pos - vector(0.2,0,0), axis=vector(-0.5,0,0), radius=0.15, color=color.orange, opacity=0.6)

    rockets.append({
        'body': body,
        'nose': nose,
        'wing_top': wing_top,
        'wing_bottom': wing_bottom,
        'flame': flame,
        'velocity': vector(0.1,0.05,0)  # sama nopeus kaikille
    })
# -------------------
# Animaatio
# -------------------
while True:
    rate(60)

   # Päivitetään tähtien liikettä
    for star in stars:
        star.pos.z += 0.1
        if star.pos.z > 2:
            star.pos.z = uniform(-20,-10)
            star.pos.x = uniform(-10,10)
            star.pos.y = uniform(-5,5)

    # Päivitetään rakettien liikettä
    for r in rockets:
        # Päivitetään nopeus (yläviistoon)
        r['velocity'] = vector(0.1, 0.1, 0)

        # Siirretään kaikki osat liikkuvan raketin mukana
        r['body'].pos += r['velocity']                    # rungon paikka päivittyy
        r['nose'].pos = r['body'].pos + r['body'].axis   # keula seuraa runkoa
        r['wing_top'].pos = r['body'].pos + vector(0.5,0.6,0)  # yläsiipi
        r['wing_bottom'].pos = r['body'].pos + vector(0.5,-0.6,0)  # alasiipi
        r['flame'].pos = r['body'].pos - vector(0.2,0,0)  # lieska

        # Reset jos raketti menee liian kauas
        if r['body'].pos.x > 10 or r['body'].pos.y > 5:
            r['body'].pos = vector(-2 - rockets.index(r)*1.5, uniform(-1,1), -5)
