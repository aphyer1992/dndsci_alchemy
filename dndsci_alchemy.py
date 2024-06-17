import math
import random

global_ingredients = [
     {'name': 'Badger Skull', 'magical' : False, 'ingredient_in' : 'Rage Potion'},
     {'name': 'Beech Bark', 'magical' : False, 'ingredient_in' : 'Barkskin Potion'},
    {'name': 'Crushed Diamond', 'magical' : False, 'ingredient_in' : 'Invisibility Potion', 'rare' : 1},
     {'name': 'Crushed Onyx', 'magical' : False, 'ingredient_in' : 'Necromantic Power Potion', 'rare' : 1},
    {'name': 'Crushed Ruby', 'magical' : False, 'ingredient_in' : 'Fire Resist Potion', 'rare' : 1},
    {'name': 'Crushed Sapphire', 'magical' : False, 'ingredient_in' : None, 'rare' : 1},
    {'name': 'Eye of Newt', 'magical' : False, 'ingredient_in' : 'Farsight Potion'},
     {'name': 'Ground Bone', 'magical' : False, 'ingredient_in' : 'Necromantic Power Potion'},
     {'name': 'Oaken Twigs', 'magical' : False, 'ingredient_in' : 'Barkskin Potion'},
    {'name': 'Powdered Silver', 'magical' : False, 'ingredient_in' : 'Glibness Potion'},
    {'name': 'Quicksilver', 'magical' : False, 'ingredient_in' : None},
     {'name': 'Redwood Sap', 'magical' : False, 'ingredient_in' : 'Growth Potion'},


    {'name': "Angel Feather", 'magical' : True, 'ingredient_in' : None, 'rare' : 1},
    {'name': "Beholder Eye", 'magical' : True, 'ingredient_in' : 'Farsight Potion', 'rare' : 1},
     {'name': "Demon Claw", 'magical' : True, 'ingredient_in' : 'Rage Potion'},
    {'name': 'Dragon Scale', 'magical' : True, 'ingredient_in' : 'Fire Resist Potion', 'rare' : 1},
    {'name': 'Dragon Spleen', 'magical' : True, 'ingredient_in' : 'Fire Breathing Potion', 'rare' : 1},
    {'name': 'Dragon Tongue', 'magical' : True, 'ingredient_in' : 'Glibness Potion', 'rare' : 1},
    {'name': "Dragon's Blood", 'magical' : True, 'ingredient_in' : 'Fire Breathing Potion', 'rare' : 1},
    {'name': 'Ectoplasm', 'magical' : True, 'ingredient_in' : 'Invisibility Potion'},
    {'name': 'Faerie Tears', 'magical' : True, 'ingredient_in' : None},
     {'name': "Giant's Toe", 'magical' : True, 'ingredient_in' : 'Growth Potion'},
     {'name': "Troll Blood", 'magical' : True, 'ingredient_in' : 'Regeneration Potion'},
     {'name': "Vampire Fang", 'magical' : True, 'ingredient_in' : 'Regeneration Potion'},
]

global_ingredients.sort(key = lambda x : x['name'])
for i in global_ingredients:
    if 'rare' not in i.keys():
        i['rare'] = 0

global_potions = []
for i in global_ingredients:
    p = i['ingredient_in']
    if p is not None and p not in global_potions:
        global_potions.append(p)

global_memory = {}
for p in global_potions:
    assert(len([i for i in global_ingredients if i['ingredient_in'] == p]) == 2)
    global_memory[p] = []
global_results = {}
global_successes = 0
global_failures = 0



def potion_result(ingredients):
    power = len([i for i in ingredients if i['magical'] == True])
    if (power <= 1) :
        return(['Inert Glop', 0, power, 0])
    if (power == 2 and random.random() < 0.5):
        return(['Inert Glop', 0, power, 0.5])
    if (power >= 5):
        return(['Magical Explosion', 0, power, 0])
    if (power == 4 and random.random() < 0.5):
        return(['Magical Explosion', 0, power, 0.5])
    inter_prob = 0.5 if power in [2,4] else 1
    potion_hits = []
    for p in global_potions:
        if(len([i for i in ingredients if i['ingredient_in'] == p]) == 2):
            potion_hits.append(p)

    if len(potion_hits) == 0:
        return(['Acidic Slurry', 0, power, 0])
    else:
        if random.random() > (1/len(potion_hits)): # if multiple potions things usually go wrong, if only one it always works
            return(['Mutagenic Ooze', 0, power, inter_prob / len(potion_hits)])
        else:
            return([random.choice(potion_hits), 1, power, inter_prob /
len(potion_hits)])

def log(row, mode='a'):
    f = open('dndsci_pot_data.csv', mode=mode)
    f.write(','.join([str(x) for x in row]) + '\n')

def random_ingredients():
    hit = False
    while hit == False:
        num_ingredients = math.ceil(random.random() * 6) + 2
        ingredients = random.sample(global_ingredients, num_ingredients)
        num_rare = len([i for i in ingredients if i['rare'] > 0])
        continue_prob = pow(0.7, num_rare)
        if random.random() < continue_prob:
            hit = True
    ingredients.sort(key = lambda x: x['name'])
    return(ingredients)

def gen_row():
    ingredients = None
    if random.random() < 0.8: # trying to make something specific as opposed to experimenting
        target_potion = random.choice(global_potions)
        recipes = global_memory[target_potion] # distinct ways we've made it in the past
        if random.random() < (0.1 * len(recipes)): # if we've only made it a few times in the past we'll often try something new
            ingredients = random.choice(recipes)

    if ingredients is None: # we are experimenting, or we didn't find a recipe we liked.
        ingredients = random_ingredients()
    result = potion_result(ingredients)
    if result[1] == 1: # success
        if ingredients not in global_memory[result[0]]:
            global_memory[result[0]].append(ingredients)
    if result[0] not in global_results.keys():
        global_results[result[0]] = 1
    else:
        global_results[result[0]] = global_results[result[0]] + 1
    out_row = []
    for i in global_ingredients:
        out_row.append( 1 if i in ingredients else 0 )

    if result[1] == 0:
        global global_failures
        global_failures = global_failures + 1
    if result[1] == 1:
        global global_successes
        global_successes = global_successes + 1

    # what could be happening here
    if result[0] == 'Barkskin Potion':
        out_row.append("Necromantic Power Potion")
    elif result[0] == 'Necromantic Power Potion':
        out_row.append('Barkskin Potion')
    else:
        out_row.append(result[0])

    out_row = out_row + result[1:]
    log(out_row)

def setup_logs():
    row = []
    for i in global_ingredients:
        row.append(i['name'])
    log(row + ['Result', 'Success?', 'power', 'p_success'], mode='w')



runs = 118453 # I am not a nice person. Not. At. All.
random.seed('D&D.Sci. Alchemy')

setup_logs()
for i in range(int(runs)):
    #if i%1e4 == 0:
        #print(i)
    gen_row()

#print('Done!')
#for i in global_results.keys():
    #print('{}: {}'.format(i, global_results[i]))

#print('{} successes, {} failures'.format(global_successes, global_failures))

# code to test and make sure the simple approach doesn't get 100%
f = open('dndsci_pot_data.csv')
lines = f.readlines()

key = lines[0]
key = key.replace('\n', '')
cols = key.split(',')
data = []

for i in range(1,len(lines)):
    row = lines[i]
    row = row.replace('\n', '')
    row = row.split(',')
    row_data = {}
    recipe = []
    for j in range(len(cols)):
        row_data[cols[j]] = row[j]
        if j < 24:
            if row[j] == '1':
                recipe.append(cols[j])
    row_data['recipe'] = ', '.join(recipe)
    row_data['index'] = i
    data.append(row_data)

missing = [
"Angel Feather",
"Beholder Eye",
"Crushed Ruby",
"Crushed Sapphire",
"Dragon Tongue",
"Dragon Scale",
"Dragon Spleen",
"Dragon's Blood",
"Ectoplasm",
"Eye of Newt",
"Faerie Tears",
"Powdered Silver",
]
target = "Barkskin Potion"
hits = [d for d in data if d['Result'] == target]



perfect_hits = []
for h in hits:
    can_make = True
    for m in missing:
        if h[m] == '1':
            can_make = False
    if can_make:
        perfect_hits.append(h)

perfect_recipes = []
for p in perfect_hits:
    r = p['recipe']
    if r not in perfect_recipes:
        perfect_recipes.append(r)
score = 1
for r in perfect_recipes:
    matches = [d for d in data if d['recipe'] == r]
    worked = [d for d in matches if d['Result'] == target]
    failed = [d for d in matches if d['Result'] != target]
    first_m = min([d['index'] for d in matches])
    first_w = min([d['index'] for d in worked])
    if len(failed):
        first_f = min([d['index'] for d in failed])
    else:
        first_f = 'never'
    winrate = matches[0]['p_success']
    if (first_m == first_w) and ('Beech Bark' in r)and ('Oaken Twigs' in r) and (float(winrate) < 1):
        print("POTENTIAL HIT!!!")
        score = score * 2
    if float(winrate) == 1:
        print("OH NO!")
        score = score * 0
    print('Recipe {} with p {} was made {} times, {} appeared {} of them.  First run: {}.  First success: {}.  First failure: {}.'.format(r, winrate, len(matches), target, len(worked), first_m, first_w, first_f))


available = [i['name'] for i in global_ingredients if i['name'] not in missing]
