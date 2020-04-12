import asyncio

class Constant:
    MAPUCHE_SQUADS = [652144868109582357, 682245125656805459, 682247440346513430, 682917973287239693,
                      682919453788471306]
    DIDON_SQUADS = [682245427722190881, 682245588389200108, 682245596324823053, 682920185547587594, 652144537535512586]

class Global:
    squadrons = None
    leaders = None
    clan_member = None
    discord_client = None
    loop = None
    mapuches = didons = None
    mapuche_history = didon_history = None
    histories = None
    full_history = None


    @classmethod
    def get_squadron_by_id(cls, target):
        for squad in cls.squadrons:
            if squad.id == target:
                return squad
        return None

    @classmethod
    def get_member_by_id(cls, discord_id):
        for member in cls.clan_member:
            if member.id == discord_id:
                return member
        return None

    @classmethod
    def get_member_by_name(cls, name):
        for member in cls.clan_member:
            if name == member.name:
                return member
        for member in cls.clan_member:
            if name in member.name:
                return member
        return None
    
    @classmethod
    def load(cls):
        from DiscordClient import DiscordClient
        cls.discord_client = DiscordClient()
        cls.loop = asyncio.get_event_loop()
        cls.loop.create_task(cls.discord_client.launch())
        cls.reload()

    @classmethod
    def reload(cls):
        cls.mapuches, cls.didons = cls.loop.run_until_complete(cls.discord_client.get_squadrons())
        cls.squadrons = cls.mapuches + cls.didons
        cls.histories = cls.loop.run_until_complete(cls.discord_client.get_full_histories())
        cls.mapuche_history, cls.didon_history = cls.histories
        cls.reload_full_history()

    @classmethod
    def reload_full_history(cls):
        from History import GlobalHistory
        cls.full_history = GlobalHistory(sum([i.matchs for i in cls.histories], []), None)
