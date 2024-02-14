import time as t






class User:
    def __init__(self,name:str):
        self.name:str = name
        self.rep:int = 0                           # 0 = neutral
        self.assoc:set[AssocType] = set()          # Set of AssocType
        self.desc = '--- No Description ---'       # Editable(?) description.
        self.evidence:set[EvidenceType] = set()    # Set of EvidenceType
        self.flags:set = set()                     # Set of FlagType
        self.createdOn = t.time()                  # Account's created time
    
    def calcRep(self):
        rep = 0

        # Associatio calculation (avg)
        if self.assoc:
            tot = 0
            for assoc in self.assoc:
                tot += assoc.rep * (assoc.ammount/2)
            tot /= (len(self.assoc)/2)
            rep += tot

        # Evidence calc
        if self.evidence:
            for ev in self.evidence:
                rep -= ev.hardness

        # Flags calc
        if self.flags:
            for flag in self.flags:
                rep -= flag.score

        rep = max(rep, -1)
        rep = min(rep, 1)

        self.rep = rep
        return rep
        

class FlagType:
    def __init__(self,type:str,confidence:int=1):
        self.type = type
        self.confidence = confidence
        self.score:float
        
        # Flag types
        if self.type == 'ClientAC': self.score = 0.2

class EvidenceType:
    def __init__(self,info:str,hardness:int,valid:bool):
        """EvidenceType

        Args:
            info (str): The evidence (yt vid link ect)
            hardness (int): How hard evidence it is (blatant = 1)
            valid (bool): Is evidence valid?
        """
        hardness = min(hardness, 1)
        if hardness < 0: self.hardness = 0
        if not valid: hardness = -0.1
        self.info = info
        self.hardness = hardness/2 # Divide by 2 to give them anohter shot at not hacking

class AssocType:
    def __init__(self,user:User,ammount:int):
        """AssocType

        Args:
            user (User): User associated with
            ammount (int): How much
        """
        self.user = user
        self.rep = user.rep
        self.ammount = ammount




a = User('Omena0')
b = User('Bank Robber')

b.evidence.add(EvidenceType('Sussy baki',1,True))
b.evidence.add(EvidenceType('Sussy baki x2',1,True))
b.flags.add(FlagType('ClientAC',1))
b.flags.add(FlagType('ClientAC',1))
b.flags.add(FlagType('ClientAC',1))
b.flags.add(FlagType('ClientAC',1))
b.calcRep()

a.assoc.add(AssocType(b,0.4))

print(a.calcRep())
print(b.calcRep())





