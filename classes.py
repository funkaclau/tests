from json import JSONDecoder, JSONEncoder


class User:
    def __init__(
        self,
        name,
        wallet,
        exploreC,
        searchC,
        homeC,
        chopC,
        mineC,
        miningXp,
        miningLvl,
        woodcutXp,
        woodcutLvl,
        craftXp,
        craftLvl,
        collectedC,
        ccoins,
        foodBank,
        events,
        events1,
        events2,
        farminglicense,
        collectorlicense,
        collectors,
        stash,
        nftout,
    ):
        self.name = name
        # self.id = id
        self.wallet = wallet
        self.exploreC = exploreC
        self.searchC = searchC
        self.homeC = homeC
        self.chopC = chopC
        self.mineC = mineC
        self.miningXp = miningXp
        self.miningLvl = miningLvl
        self.woodcutXp = woodcutXp
        self.woodcutLvl = woodcutLvl
        self.craftXp = craftXp
        self.craftLvl = craftLvl
        self.collectedC = collectedC
        self.ccoins = ccoins
        self.foodBank = foodBank
        self.events = events
        self.events1 = events1
        self.events2 = events2
        self.farminglicense = farminglicense
        self.collectorlicense = collectorlicense
        self.stash = stash
        self.collectors = collectors
        self.nftout = nftout


class Stash:
    def __init__(self, stashlocation, stashlevel, stashspace, stashinv, tools, hut):
        self.stashlocation = stashlocation
        self.stashlevel = stashlevel
        self.stashspace = stashspace
        self.stashinv = stashinv
        self.tools = tools
        self.hut = hut


class Stashmissing:
    def __init__(
        self, woodmissing, stonemissing, claymissing, nailmissing, ropemissing
    ):
        self.woodmissing = woodmissing
        self.stonemissing = stonemissing
        self.claymissing = claymissing
        self.nailmissing = nailmissing
        self.ropemissing = ropemissing


class Hut:
    def __init__(self, hutlevel, fire, tools, install):
        self.hutlevel = hutlevel
        self.fire = fire
        self.tools = tools
        self.install = install


class Hutmissing:
    def __init__(
        self, woodmissing, stonemissing, claymissing, nailmissing, ropemissing
    ):
        self.woodmissing = woodmissing
        self.stonemissing = stonemissing
        self.claymissing = claymissing
        self.nailmissing = nailmissing
        self.ropemissing = ropemissing


class Tools:
    def __init__(
        self,
        knife,
        woodframe,
        fireplace,
        fpan,
        pan,
        bowl,
        dish,
        jar,
        bamboocup,
        woodspoon,
        woodspatula,
    ):
        self.knife = knife
        self.woodframe = woodframe
        self.fireplace = fireplace
        self.fpan = fpan
        self.pan = pan
        self.bowl = bowl
        self.dish = dish
        self.jar = jar
        self.bamboocup = bamboocup
        self.woodspoon = woodspoon
        self.woodspatula = woodspatula


class Instal:
    def __init__(
        self,
        fireplace,
        mudfurnace,
        mattress,
        pillow,
        grinder,
        table,
        compostbin,
        garden,
    ):
        self.fireplace = fireplace
        self.mudfurnace = mudfurnace
        self.mattress = mattress
        self.pillow = pillow
        self.grinder = grinder
        self.table = table
        self.compostbin = compostbin
        self.garden = garden


class Garden:
    def __init__(self, cactus):
        self.cactus = cactus


# Nested Class 1
class Collectors:
    def __init__(
        self,
        owner,
        assetID,
        daring,
        number,
        tired,
        hungry,
        morale,
        maxinv,
        inv,
        actions,
        actionsMax,
        energy,
        location,
        distance,
        gear,
    ):
        self.owner = owner
        self.assetID = assetID
        self.daring = daring
        self.number = number
        self.tired = tired
        self.hungry = hungry
        self.morale = morale
        self.maxinv = maxinv
        self.inv = inv
        self.actions = actions
        self.actionsMax = actionsMax
        self.energy = energy
        self.location = location
        self.distance = distance
        self.gear = gear


# Nested Class 2
class Gear:
    def __init__(
        self,
        belt,
        belttype,
        clover,
        clovertype,
        tele,
        bag,
        bagtype,
        boots,
        bootstype,
        axe,
        axetype,
        axesharp,
        axesharpC,
        pick,
        picktype,
        picksharp,
        picksharpC,
        compass,
        scythe,
        scythetype,
        scythesharp,
        scythesharpC,
        torch,
        torchlight,
    ):
        self.belt = belt
        self.belttype = belttype
        self.clover = clover
        self.clovertype = clovertype
        self.tele = tele
        self.bag = bag
        self.bagtype = bagtype
        self.boots = boots
        self.bootstype = bootstype
        self.axe = axe
        self.axetype = axetype
        self.axesharp = axesharp
        self.axesharpC = axesharpC
        self.pick = pick
        self.picktype = picktype
        self.picksharp = picksharp
        self.picksharpC = picksharpC
        self.compass = compass
        self.scythe = scythe
        self.scythetype = scythetype
        self.scythesharp = scythesharp
        self.scythesharpC = scythesharpC
        self.torch = torch
        self.torchlight = torchlight


class Market:
    def __init__(self, coins, rawmaterials, food, manufactured, tools, install):
        self.coins = coins
        self.rawmaterials = rawmaterials
        self.food = food
        self.manufactured = manufactured
        self.tools = tools
        self.install = install


class Food:
    def __init__(self, fc, berries, bfig, orange, fig):
        self.fc = fc
        self.berries = berries
        self.bfig = bfig
        self.orange = orange
        self.fig = fig


class Rawmaterials:
    def __init__(
        self,
        seed,
        grass,
        leaf,
        excrement,
        rag,
        bone,
        wood,
        pinecone,
        tbark,
        gmushroom,
        amanita,
        whitestone,
        granite,
        seagullegg,
        gravel,
        whetstone,
        bfstone,
        dwood,
        shell,
        fstone,
        clam,
        swater,
        rnail,
        rneedle,
        rspike,
        resin,
        bamboo,
    ):
        self.seed = seed
        self.grass = grass
        self.leaf = leaf
        self.excrement = excrement
        self.rag = rag
        self.bone = bone
        self.wood = wood
        self.pinecone = pinecone
        self.tbark = tbark
        self.gmushroom = gmushroom
        self.amanita = amanita
        self.whitestone = whitestone
        self.granite = granite
        self.seagullegg = seagullegg
        self.gravel = gravel
        self.whetstone = whetstone
        self.bfstone = bfstone
        self.dwood = dwood
        self.shell = shell
        self.fstone = fstone
        self.clam = clam
        self.swater = swater
        self.rnail = rnail
        self.rneedle = rneedle
        self.rspike = rspike
        self.resin = resin
        self.bamboo = bamboo


class Manufactured:
    def __init__(
        self,
        bhook,
        wrope,
        woodboard,
        wframe,
        wfence,
        rcpot,
        rcpan,
        rcjar,
        rcdish,
        rcbowl,
        epellets,
        rccup,
        bamboocup,
        rcbrick,
        ebrick,
    ):
        self.bhook = bhook
        self.wrope = wrope
        self.woodboard = woodboard
        self.wframe = wframe
        self.wfence = wfence
        self.rcpot = rcpot
        self.rcpan = rcpan
        self.rcjar = rcjar
        self.rcdish = rcdish
        self.rcbowl = rcbowl
        self.epellets = epellets
        self.rccup = rccup
        self.bamboocup = bamboocup
        self.rcbrick = rcbrick
        self.ebrick = ebrick


# json decoder class
class UserDecoder(JSONDecoder):
    def default(self, o):
        return o.__dict__


class MarketDecoder(JSONDecoder):
    def default(self, o):
        return o.__dict__


# json encoder class
class UserEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
