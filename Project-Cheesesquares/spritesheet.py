import pygame

class _Spritesheet:
    """
    Class for extracting parts of images.
    
    Should not be used directly. Use AnimatedSprite instead.
    """
    def __init__(self,image,use_alpha=False):
        """
        Creates a new Spritesheet.
        
            image       : path
            [use_alpha] : boolean
        """
        if not use_alpha: self.sheet = pygame.image.load(image).convert()
        else: self.sheet = pygame.image.load(image)#.convert_alpha()
            
    def get_at(self,rect):
        """
        gets a image at the given position.
        
            rect : pygame.rect.Rect
            
            -> pygame.Surface
        """
        image = pygame.Surface(rect.size,flags = pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        #image.convert_alpha()
        
        return image
        
    def images_at(self, rects):
        """
        Loads multiple images, supply a list of coordinates
        
            rect : pygame.rect.Rect[]
            
            -> pygame.Surface[]
        """
        return [self.get_at(rect) for rect in rects]
    
    def image_strip(self, rect, amount):
        """
        Loads all Images in a strip with lenght amount. Image size is the rects size and begin point is the rects x/y-Position.
        
            rect   : pygame.rect.Rect
            amount : int
            
            -> pygame.Surface[]
        """
        images = []
        for i in range(amount):
            #print(i*rect.w)
            images.append(self.get_at(pygame.rect.Rect(rect.x+i*rect.w,rect.y,rect.w,rect.h)))
        return images
    
    def _abandon_sheet(self):
        """
        deletes the sheet. Should only be called after extracting all the animations
            
            --no arguments--
        """
        del self.sheet
        
class AnimatedSprite(_Spritesheet):
    """
    Class for handling Animations out of Spritesheets.
    """
    def __init__(self,image,animations,size,use_alpha=False):
        """
        Creates a new AnimatedSprite.
        
            image       : path
            animations  : dict[ str : int ]    -- Name : Frame count, different animations under each other.
                                                  Pos = image Position
            size        : pygame.math.Vector2  -- Size of images
            [use_alpha] : boolean
        """
        super().__init__(image,use_alpha)
        self.size = size
        self.animations = {}
        self.current_animation = "idle"
        i = 0
        for anim in animations.keys():
            self.animations[anim] = self.image_strip(pygame.rect.Rect(0,int(i*size.y),size.x,size.y),animations[anim])
            i+=1
        self._abandon_sheet()
        #print(self.animations)
    def set_animation(self,name='idle'):
        """
        sets the current animation (standard 'idle'). Will not set if not included.
        
            [name] : str
        """
        if name in self.animations.keys():
            self.current_animation = name
    
    def get_image(self,frame):
        """
        get the current-frame image
        
            frame : int
            
            -> pygame.Surface
        """
        return self.animations[self.current_animation][frame % len(self.animations[self.current_animation])]
