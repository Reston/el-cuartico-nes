-- Independent PPU-level checks: no game memory or save states are modified.
local root=PROJECT_ROOT
local labels={}
for line in io.lines(root..'build/el-cuartico.lbl') do
 local addr,name=line:match('al (%x+) %.(_[%w_]+)')
 if addr then labels[name]=tonumber(addr,16) end
end
local report=assert(io.open(root..'build/mesen-presentation-tests.txt','w'))
local function r(name,offset)return emu.read(assert(labels['_'..name])+(offset or 0),emu.memType.nesDebug)end
local function check(ok,label)
 report:write((ok and 'PASS ' or 'FAIL ')..label..'\n');report:flush()
 if not ok then error(label) end
end
local input={}
local function frames(n,buttons)
 for _=1,n do input=buttons or {};coroutine.yield() end
end
local function press(button)
 frames(2,{[button]=true});frames(6)
end
local function bytes(address,count,kind)
 local data={}
 for i=0,count-1 do data[#data+1]=string.char(emu.read(address+i,kind)) end
 return table.concat(data)
end
local function picture()return bytes(0x2000,1024,emu.memType.nesPpuDebug)end
local function palette()return bytes(0x3f00,32,emu.memType.nesPpuDebug)end
local function row(y)return bytes(0x2000+y*32+2,28,emu.memType.nesPpuDebug):gsub('%z',' ')end
local function state()
 local list={'mode','host','completed','seconds','tick','health','misses','task_active','task_phase','task_progress','task_value','rng','hits','found','count_in','song_tick','song_step','music_act','rhythm_phase','chart_step','anim_tick'}
 local data={}
 for _,name in ipairs(list) do data[#data+1]=r(name) end
 for _,entry in ipairs({{'alarm',4},{'task_frame',2},{'task_code',4},{'task_order',3},{'note_age',3},{'note_live',3},{'attempt_score',2}}) do
  for i=0,entry[2]-1 do data[#data+1]=r(entry[1],i) end
 end
 return table.concat(data,',')
end
local function pause_check(label)
 if r('mode')~=2 and r('task_active')==0 then
  for _=1,100 do if r('tick')>=15 and r('tick')<30 then break end;frames(1) end
 end
 frames(4)
 local nt,pal=picture(),palette()
 press('start')
 check(r('paused')==1 and row(10):find('PAUSA',1,true)~=nil,'Pause slate is visible: '..label)
 check(bytes(0x5c00,1024,emu.memType.nesDebug)==nt,'ExRAM captures all 1024 nametable bytes: '..label)
 check(bytes(labels._pause_palette,32,emu.memType.nesDebug)==pal,'Pause captures all 32 palette entries: '..label)
 local frozen=state()
 press('select');frames(120)
 check(r('pause_help')==1 and row(10):find('COMO JUGAR',1,true)~=nil and state()==frozen,'Contextual controls freeze the same game state: '..label)
 check(bytes(0x5c00,1024,emu.memType.nesDebug)==nt,'Controls do not overwrite the saved picture: '..label)
 press('b');press('start');frames(4)
 check(r('paused')==0 and picture()==nt,'Resume restores the complete nametable: '..label)
 check(palette()==pal,'Resume restores the complete palette: '..label)
end
local function leave_game()
 press('start');press('b');check(r('mode')==0,'Pause exit returns to menu')
end
local function launch(host)
 assert(r('mode')==0)
 for _=1,3 do if r('host')==host then break end;press('right') end
 press('a');assert(r('mode')==7);press('a')
 frames(20);assert(r('mode')==host+1)
end
local function go(x,y)
 for _=1,600 do
  local px,py=r('px'),r('py');if px==x and py==y then return end
  local tx,ty=x,y
  if py<140 and ((px<128)~=(x<128)) then tx,ty=px<128 and 32 or 208,144 end
  if px~=tx then frames(1,{[px<tx and 'right' or 'left']=true})
  else frames(1,{[py<ty and 'down' or 'up']=true}) end
 end
 error('Station approach timed out')
end
local function district(wanted)
 for _=1,1000 do
  if r('district')==wanted and r('hud_on')==1 then frames(15);return end
  local d=r('district')
  if d%2~=wanted%2 then frames(1,{[d%2<wanted%2 and 'right' or 'left']=true})
  else frames(1,{[d<wanted and 'down' or 'up']=true}) end
 end
 error('District crossing timed out')
end
local function find_daniel()
 district(r('target_district'))
 for _=1,600 do
  local t=r('target');local x,y=r('npc_x',t),r('npc_y',t)+4
  if r('cursor_x')~=x then frames(1,{[r('cursor_x')<x and 'right' or 'left']=true})
  elseif r('cursor_y')~=y then frames(1,{[r('cursor_y')<y and 'down' or 'up']=true})
  else press('a');frames(55);return end
 end
 error('Search target was not reachable')
end
local total_frames=0
local runner=coroutine.create(function()
 frames(90)
 press('up');check(r('mode')==8 and row(14):find('12 REPARACIONES',1,true)~=nil,'Menu help contains the actual Chucho objective')
 press('right');check(row(14):find('20 ACIERTOS',1,true)~=nil,'Menu help changes with the selected character')
 press('b');launch(0);pause_check('live studio');leave_game()
 for station=0,3 do
  launch(0);go(station%2==0 and 32 or 208,station<2 and 64 or 136)
  for _=1,900 do if r('alarm',station)>0 then break end;frames(1) end
  press('a');assert(r('task_active')==1 and r('repair_task')==station)
  pause_check('repair panel '..station);press('b');leave_game()
 end
 launch(1);pause_check('rhythm practice');press('a')
 local next_act=1
 for _=1,2400 do
  if r('music_act')==next_act then
   pause_check('musical act '..(next_act+1));next_act=next_act+1
   if next_act==3 then break end
  end
  local head=r('cue_head')
  if head<3 and r('note_age',head)==90 then frames(1,{[({'a','b','left','right','up','down'})[r('note_key',head)+1]]=true})
  else frames(1) end
 end
 check(next_act==3 and r('misses')==0,'Act lighting and note timing survive pause and help')
 leave_game();launch(2);pause_check('first plaza');find_daniel()
 assert(r('round_no')==1);district(1);pause_check('banked market');find_daniel()
 assert(r('round_no')==2);district(3);pause_check('banked neighborhood');find_daniel()
 check(r('mode')==4 and row(10):find('TOMA PERFECTA',1,true)~=nil,'Search victory renders the new success heading')
 check(row(18):find('03/03',1,true)~=nil and row(22):find('1/3 SELLOS',1,true)~=nil,'Result card shows correct objective and episode progress')
 local file=assert(io.open(root..'build/mesen-presentation-result.png','wb'));file:write(emu.takeScreenshot());file:close()
 press('a');check(r('mode')==0 and row(10):find('1/3 SELLOS',1,true)~=nil,'Returning to menu retains the visible earned seal')
 report:close();emu.stop(0)
end)
emu.addEventCallback(function()
 total_frames=total_frames+1
 if total_frames>14000 then report:write('FAIL timeout\n');report:close();emu.stop(2);return end
 local ok,err=coroutine.resume(runner)
 if not ok then
  report:write('FAIL '..tostring(err)..'\n');report:close();emu.stop(1);return
 end
 local controller={a=false,b=false,start=false,select=false,up=false,down=false,left=false,right=false}
 for name,value in pairs(input) do controller[name]=value end
 emu.setInput(controller,0)
end,emu.eventType.inputPolled)
