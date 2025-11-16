class Place:
    def __init__(self, name, _type, found, zone, x, y):
        self.name = name
        self._type = _type
        self.found = found
        self.zone = zone
        self.x = x
        self.y = y
        self.length = max(abs(self.x), abs(self.y))

    def __str__(self):
        return f'{self.name}\n{self._type}\n{self.found}\n{self.zone}\n{self.x}\n{self.y}\n'


class User:
    def __init__(self, uid, username, name, squad_name, time, res_time, deff, attack, health_p, power_p, mana_p, role,
                 boss_ping, city, prof, prof_time, timezone, trap, rest, kk):
        self.uid = uid
        self.city = city
        self.res_time = res_time
        self.deff = deff
        self.attack = attack
        self.username = username
        self.name = name
        self.squad_name = squad_name
        self.time = time
        self.mana_p = mana_p
        self.power_p = power_p
        self.health_p = health_p
        self.role = role
        self.boss_ping = boss_ping
        self.prof = prof
        self.prof_time = prof_time
        self.timezone = timezone
        self.trap = trap
        self.rest = rest
        self.kk = kk

    def __len__(self):
        try:
            n = 0
            _m = self.prof.split(' ')
            n += int(_m[3])
            n += 0 if _m[2] == 'Новичок' else 30 if _m[2] == 'Адепт' else 60
            return n
        except:
            return 1000000

    def __str__(self):
        return f'{self.uid}\n{self.username}\n{self.name}\n{self.squad_name}\n{self.time}\n{self.res_time}\n{self.deff}\n{self.attack}\n{self.health_p}\n{self.power_p}\n{self.mana_p}\n{self.role}\n{self.boss_ping}\n{self.city}\n{self.prof}\n{self.prof_time}\n{self.timezone}\n{self.trap}\n{self.rest}\n{self.kk}\n'


class Raid_poll:
    def __init__(self, poll_id, off_id):
        self.opazdyvayu = []
        self.v_shage = []
        self.na_tochke = []
        self.idu = []
        self.off_id = off_id
        self.raid_poll_id = poll_id

    def __str__(self):
        return f'{str(self.idu)}, {str(self.na_tochke)}, {str(self.v_shage)},{str(self.opazdyvayu)}'

    def __len__(self):
        return 1


class Raid:
    def __init__(self, name, time, zone):
        self.city = '🕧None'
        self.time = time
        self.name = name
        self.IsUnderAttack = False
        self.IsValid = False
        self.zone = zone

    def __str__(self):
        return f'{self.name}\n{self.IsValid}\n{self.IsUnderAttack}\n{self.time}\n{self.city}\n'
class Map:
    def __init__(self, colors, objects):
        self.colors=colors
        self.objects=objects
    def __str__(self):
        s=''
        for i in range(21):
            for j in range(21):
                s+=str(self.colors[i][j])
            s+='\n'
        for i in range(21):
            for j in range(21):
                s+=self.objects[i][j]
            s+='\n'
        return s



