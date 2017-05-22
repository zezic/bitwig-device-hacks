from lib import atoms

modulator = (atoms.Modulator('Test')
    .description('Test device'))

print(modulator.build_meta())
print(modulator.build())
