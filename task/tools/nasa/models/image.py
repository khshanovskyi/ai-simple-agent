from dataclasses import dataclass, field


@dataclass
class Image:
    id: int
    sol: int
    img_src: str
    content_length: int = 0


@dataclass
class ImageList:
    photos: list[Image] = field(default_factory=list)