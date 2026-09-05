local f=0
emu.addEventCallback(function()
 f=f+1
 if f==90 then
  emu.log('SMOKE FRAME 90')
  local png=emu.takeScreenshot()
  local file=assert(io.open(PROJECT_ROOT..'build/title.png','wb'))
  file:write(png);file:close()
  emu.stop(0)
 end
end,emu.eventType.endFrame)
