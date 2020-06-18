from moviepy.editor import VideoFileClip, CompositeVideoClip

clip = (VideoFileClip("D:\Documents\studia\semestr4\Arena-of-Heroes\demo\\move.mp4")
        .subclip((0, 5.8), (0, 8))
        .speedx(0.4)
        .crop(x1=290, y1=236, x2=552, y2=563)
        )
# clip.show(interactive=True)
d = clip.duration
snapshot = (clip.to_ImageClip()
            .set_duration(d/6)
            .crossfadein(d/6)
            .set_start(5*d/6))
composition = CompositeVideoClip([clip, snapshot])
composition.write_gif('carry.gif', fps=clip.fps, fuzz=0)
composition.write_gif("D:\Documents\studia\semestr4\Arena-of-Heroes\demo\\move.gif")