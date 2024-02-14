import time as t





class User:
    def __init__(self,name:str):
        self.name:str = name
        self.rep:int = 0                           # Positive = good, negative = bad, 0 = Neutral/unknown
        self.assoc:set[AssocType] = set()          # Set of AssocType
        self.desc = '--- No Description ---'       # Editable(?) description.
        self.evidence:set[EvidenceType] = set()    # Set of EvidenceType
        self.flags:set = set()                     # Set of FlagType
        self.createdOn = t.time()                  # Account's created time
    
    def calcRep(self,called_from=None):
        rep = 0

        # Association calculation
        if self.assoc:
            for i in self.assoc:
                if called_from == i.user: continue
                rep += round(i.user.calcRep(called_from=self) * i.ammount,4)/10

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
        rep = round(rep,4)
        
        self.rep = rep
        return rep


users:list[User] = []


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















