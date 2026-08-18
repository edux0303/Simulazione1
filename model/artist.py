from dataclasses import dataclass


@dataclass
class Artist:
    ArtistId: int
    Name: str



    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return isinstance(other, Artist) and self.ArtistId == other.ArtistId

    def __str__(self):
        return self.Name