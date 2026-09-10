-- Independent PPU/video checks for character cards and atomic help updates.
-- Controller input is the only way this test changes the running game.
local root=PROJECT_ROOT
local labels={}
for line in io.lines(root..'build/el-cuartico.lbl')do
 local addr,name=line:match('al (%x+) %.(_[%w_]+)')
 if addr then labels[name]=tonumber(addr,16)end
end
local report=assert(io.open(root..'build/mesen-usability-tests.txt','w'))
local function r(name,i)return emu.read(assert(labels['_'..name])+(i or 0),emu.memType.nesDebug)end
local function check(ok,label)
 report:write((ok and 'PASS ' or 'FAIL ')..label..'\n');report:flush()
 if not ok then error(label)end
end
local input={}
local function frames(n,buttons)for _=1,n do input=buttons or {};coroutine.yield()end end
local function press(key)frames(5,{[key]=true});frames(15)end
local function bytes(address,count,kind)
 local out={};for i=0,count-1 do out[#out+1]=string.char(emu.read(address+i,kind))end;return table.concat(out)
end
local function page()return bytes(0x2000,1024,emu.memType.nesPpuDebug)end
-- Tile 0 and ASCII space have identical blank glyphs in the shared slate.
local function help_page()local p=page();return p:sub(1,960):gsub('%z',' ')..p:sub(961)end
local function row(y)return bytes(0x2000+y*32,32,emu.memType.nesPpuDebug)end
local function shot(name)local f=assert(io.open(root..'build/'..name..'.png','wb'));f:write(emu.takeScreenshot());f:close()end
local runner=coroutine.create(function()
 frames(90)
 for host=0,2 do
  while r('host')~=host do press('right')end
  frames(90,{a=true});frames(4)
  check(r('mode')==7 and r('ex_on')==2 and r('hud_on')==0,'Holding A stays on the illustrated title card for host '..host)
  local names={'chucho','estefania','dany'}
  local f=assert(io.open(root..'assets/'..names[host+1]..'-intro.nam','rb'));local expected=f:read(960);f:close()
  check(page():sub(1,960)==expected,'Host '..host..' title card maps all 960 tiles from the correct PRG data bank')
  local map,video=page(),emu.takeScreenshot();local seconds,tick=r('seconds'),r('tick')
  frames(300)
  check(page()==map and emu.takeScreenshot()==video and r('seconds')==seconds and r('tick')==tick,'Host '..host..' title card remains static and untimed in Mesen')
  shot('mesen-title-'..host);press('b')
  check(r('mode')==0 and r('host')==host and r('ex_on')==1,'B restores the selected portrait after host '..host..' card')
  press('start');assert(r('mode')==7);press('start')
  check(r('mode')==host+1 and r('paused')==0 and r('misses')==0,'Start confirms host '..host..' without pausing or consuming a guess')
  press('start');press('a');assert(r('mode')==7);press('b')
 end
 while r('host')~=0 do press('right')end
 press('up')
 local pages,videos={},{}
 for host=0,2 do
  pages[help_page()]=true;videos[emu.takeScreenshot()]=true
  if host==1 then
   check(row(16):find('DERECHA A IZQ.',1,true)~=nil and row(18):find('AL LLEGAR AL MARCO',1,true)~=nil,'Estefania help explains the moving notes and the timing target')
  end
  press('right')
 end
 local bad,stalls,video_bad=0,0,0
 for loop=1,5 do
  for _,key in ipairs({'right','right','right','left','left','left','select','select','select'})do
   for frame=1,4 do
    local anim=r('anim_tick');frames(1,frame==1 and {[key]=true} or {})
    if not pages[help_page()]then bad=bad+1 end
    if not videos[emu.takeScreenshot()]then video_bad=video_bad+1 end
    if (r('anim_tick')-anim)%256~=1 then stalls=stalls+1 end
   end
  end
 end
 check(bad==0,'Rapid help switching keeps the complete PPU text layout and attributes intact')
 check(video_bad==0,'Every rendered help frame exactly matches a complete page, including its borders')
 check(stalls==0 and r('help_dirty')==0,'Help switching maintains 60 Hz and completes the vblank upload')
 press('right');shot('mesen-help-estefania');press('b');press('a')
 check(r('mode')==7 and r('host')==1,'Help can launch Estefania through the new title card')
 report:close();emu.stop(0)
end)
local total=0
emu.addEventCallback(function()
 total=total+1
 if total>6000 then report:write('FAIL timeout\n');report:close();emu.stop(2);return end
 local ok,err=coroutine.resume(runner)
 if not ok then report:write('FAIL '..tostring(err)..'\n');report:close();emu.stop(1);return end
 local controller={a=false,b=false,start=false,select=false,up=false,down=false,left=false,right=false}
 for name,value in pairs(input)do controller[name]=value end
 emu.setInput(controller,0)
end,emu.eventType.inputPolled)
