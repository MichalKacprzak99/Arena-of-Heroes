from moviepy.editor import *

clip = (VideoFileClip("D:\Documents\studia\semestr4\Arena-of-Heroes\demo\\attack.mp4")
        .subclip((0, 6), (0, 7))
        .speedx(0.4)
        .crop(x1=611, y1=485, x2=800, y2=660)
        )
# clip.show(interactive=True)
d = clip.duration
snapshot = (clip.to_ImageClip()
            .set_duration(d/6)
            .crossfadein(d/6)
            .set_start(5*d/6))
composition = CompositeVideoClip([clip, snapshot])
composition.write_gif('carry.gif', fps=clip.fps, fuzz=3)
composition.write_gif("D:\Documents\studia\semestr4\Arena-of-Heroes\demo\\attack.gif")