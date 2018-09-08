set WLAPath=.\
set ProjectName=done

echo [objects] > temp.prj
echo %ProjectName%.obj >> temp.prj

# windows, whatever habe ich nicht getestet
%WLAPath%\wla-65816.exe -o %ProjectName%.asm %ProjectName%.obj
%WLAPath%\wlalink.exe -vr temp.prj %ProjectName%.smc

# mac
krings@mbp wla_tik-tak-toe $ wla-65816 -o done.obj done.asm
krings@mbp wla_tik-tak-toe $ wlalink -v -r temp.prj temp.smc

del %ProjectName%.obj
del temp.prj

pause