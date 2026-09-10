-- Independent two-episode campaign, controller input and real PPU inspection.
local root=PROJECT_ROOT
local labels={}
for line in io.lines(root..'build/el-cuartico.lbl') do
 local addr,name=line:match('al (%x+) %.(_[%w_]+)')
 if addr then labels[name]=tonumber(addr,16) end
end
local report=assert(io.open(root..'build/mesen-second-episode-tests.txt','w'))
local function r(name,i)return emu.read(assert(labels['_'..name])+(i or 0),emu.memType.nesDebug)end
local function check(ok,label)
 report:write((ok and 'PASS ' or 'FAIL ')..label..'\n');report:flush()
 if not ok then error(label) end
end
local input={}
local function frames(n,buttons)for _=1,n do input=buttons or {};coroutine.yield() end end
local function press(button)frames(5,{[button]=true});frames(15)end
local function bytes(address,count,kind)
 local data={};for i=0,count-1 do data[#data+1]=string.char(emu.read(address+i,kind))end;return table.concat(data)
end
local function row(y)return bytes(0x2000+y*32,32,emu.memType.nesPpuDebug):gsub('%z',' ')end
local function shot(name)local f=assert(io.open(root..'build/'..name..'.png','wb'));f:write(emu.takeScreenshot());f:close()end
local keys={'a','b','left','right','up','down'}
local function one(key)return {[key]=true}end
local function task_input(f)
 local t,p,tap=r('repair_task'),r('task_progress'),f%4<2
 if t==0 then
  local wanted=0;for i=0,2 do if r('task_order',i)==p then wanted=i end end
  if not tap then return {}end;return one(r('task_cursor')==wanted and 'a' or 'down')
 elseif t==1 then
  local v,w=r('task_value'),r('task_target')
  if v~=w then return one(v<w and 'right' or 'left')end
  return tap and one('a') or {}
 elseif t==2 then return tap and math.abs(r('task_value')-r('task_target'))<=3 and one('a') or {}
 else return r('task_phase')~=0 and tap and one(keys[r('task_code',p)+3]) or {} end
end
local function repair_input(f)
 if r('task_active')==1 then return task_input(f)end
 local target,deadline=nil,255
 for i=0,3 do if r('alarm',i)>0 and r('alarm',i)<deadline then target,deadline=i,r('alarm',i)end end
 if target==nil then return {}end
 if r('episode')==1 and r('alarm',1)>0 and r('alarm',2)>0 then target=math.floor(r('repairs')/4)%2==0 and 2 or 1 end
 local x,y=target%2==0 and 32 or 208,target<2 and 64 or 136
 local px,py=r('px'),r('py')
 if py<140 and ((px<128)~=(x<128))then x,y=px<128 and 32 or 208,144 end
 local result={}
 if math.abs(px-x)>2 then result[px<x and 'right' or 'left']=true
 elseif math.abs(py-y)>2 then result[py<y and 'down' or 'up']=true
 else return f%4<2 and one('a') or {}end
 if r('cooldown')==0 then result.b=true end;return result
end
local function rhythm_input()
 if r('cue_demo')==1 then return one('a')end
 if r('hold_slot')<3 then return one(keys[r('note_key',r('hold_slot'))+1])end
 local head=r('cue_head');return head<3 and r('note_age',head)==90 and one(keys[r('note_key',head)+1]) or {}
end
local function search_input(props)
 if r('search_wait')>0 or r('feedback')>0 then return {}end
 local wanted,x,y=r('target_district'),nil,nil
 if props and r('episode')==1 and r('prop_mask')~=3 then
  local item=r('prop_mask')%2==0 and 0 or 1
  wanted,x,y=r('prop_area',item),r('prop_x',item),80
 end
 local d=r('district')
 if d~=wanted then
  if d%2~=wanted%2 then return one(d%2<wanted%2 and 'right' or 'left')end
  return one(d<wanted and 'down' or 'up')
 end
 if x==nil then x,y=r('npc_x',r('target')),r('npc_y',r('target'))+4 end
 if r('cursor_x')~=x then return one(r('cursor_x')<x and 'right' or 'left')end
 if r('cursor_y')~=y then return one(r('cursor_y')<y and 'down' or 'up')end
 return one('a')
end
local function select(host)
 assert(r('mode')==0)
 for _=1,3 do if r('host')==host then return end;press('right')end
 error('Host selection failed')
end
local function launch(host)
 select(host);press('a')
 if r('episode')==1 then
  check(r('mode')==9 and row(10):find('EPISODIO 2',1,true)~=nil,'Episode-two briefing renders correctly for host '..host)
  local seconds,score=r('seconds'),r('score')+r('score',1)*256
  frames(125)
  check(r('seconds')==seconds and r('score')+r('score',1)*256==score,'Briefing freezes the clock and score for host '..host)
  press('a')
 else assert(r('mode')==7);press('a')end
 frames(30);assert(r('mode')==host+1)
end
local function snapshot(list)
 local out={};for _,name in ipairs(list)do out[#out+1]=r(name)end;return table.concat(out,',')
end
local function pause_scene(label,held)
 press('start');assert(r('paused')==1)
 local picture=bytes(0x5c00,1024,emu.memType.nesDebug)
 local saved_palette=bytes(labels._pause_palette,32,emu.memType.nesDebug)
 local fields={'seconds','tick','health','hits','misses','repairs','link_mask','prop_mask','collected_props','hold_left','song_step','song_tick','rhythm_phase'}
 local frozen=snapshot(fields)
 press('select');frames(90)
 check(snapshot(fields)==frozen and bytes(0x5c00,1024,emu.memType.nesDebug)==picture,'Help preserves state and the saved scene: '..label)
 press('b');press('start')
 if held then
  check(r('hold_resume')==1 and snapshot(fields)==frozen,'Paused sustained note waits for re-grip with its exact remaining duration')
  check(row(3):find('RETOMA EL BOTON PARA SEGUIR',1,true)~=nil,'The final held note displays its re-grip instruction instead of the outro')
  frames(120);check(snapshot(fields)==frozen,'Re-grip prompt freezes note motion and music')
 end
 -- The context row intentionally changes to the re-grip prompt after a held note.
 check(bytes(0x2080,896,emu.memType.nesPpuDebug)==picture:sub(129),'Restored playfield and attributes are exact: '..label)
 check(bytes(0x3f00,32,emu.memType.nesPpuDebug)==saved_palette,'Restored palette is exact: '..label)
end
local runner=coroutine.create(function()
 frames(90)
 for episode=0,1 do
  check(r('episode')==episode and r('completed')==0,'Episode '..(episode+1)..' begins with fresh stamps')
  for _,host in ipairs({0,2,1})do
   launch(host)
   local trace,acts={},{};local did_pause=false;local extra_cues=0
   for f=1,17000 do
    if r('mode')<1 or r('mode')>3 then break end
    if r('hud_on')==0 then frames(1)
    else
     if episode==1 and not did_pause and ((host==0 and r('task_active')==1)or(host==2 and r('prop_mask')==1)or(host==1 and r('hold_slot')<3 and r('hits')==48))then
      pause_scene('episode 2 host '..host,host==1);did_pause=true
     end
     if host==1 and r('cue_demo')==0 and not acts[r('music_act')]then
      acts[r('music_act')]=true
      check(r('music_track')==(episode==1 and 8+r('music_act')or(r('music_act')==0 and 2 or 5+r('music_act'))),'Correct composition in episode '..(episode+1)..' act '..(r('music_act')+1))
     end
     if host==1 and r('cue_demo')==0 and r('count_in')==0 then
      local count=r('hits');for i=0,2 do count=count+r('note_live',i)end
      local limits=episode==1 and {17,33,49}or{7,13,20}
      if count>limits[r('music_act')+1]then extra_cues=extra_cues+1 end
     end
     local before,station=r('repairs'),r('repair_task')
     frames(1,host==0 and repair_input(f)or(host==1 and rhythm_input()or search_input(true)))
     if host==0 and r('repairs')~=before then trace[#trace+1]=station end
    end
   end
   frames(25)
   check(r('last_win')==1 and r('medals',host)==3,'Controller play earns a perfect medal: episode '..(episode+1)..' host '..host)
   if host==0 and episode==1 then check(table.concat(trace,',')=='0,2,1,3,0,1,2,3,0,2,1,3','Both camera/mixer orders complete three linked broadcasts')end
   if host==1 then
    check(r('hits')==(episode==1 and 49 or 20),'Rhythm objective is correct for episode '..(episode+1))
    check(extra_cues==0 and r('note_live',0)+r('note_live',1)+r('note_live',2)==0,'Every act stops spawning extra notes and the final lane clears in episode '..(episode+1))
   end
   if host==2 and episode==1 then
    check(r('collected_props')==6 and r('found')==3,'All six optional props and three Daniel encounters are reachable')
    check(row(18):find('DANY 3/3  OBJETOS 6/6',1,true)~=nil,'Optional inventory is accurate on the result card');shot('mesen-episode2-props-result')
   end
   if r('mode')==4 then press('a')end
  end
  check(r('mode')==5 and r('completed')==7,'All three missions reach episode '..(episode+1)..' closure')
  if episode==0 then
   check(r('remix_unlocked')==0,'Remix remains locked after only one episode')
   local score=r('score')+r('score',1)*256;press('a')
   check(r('episode')==1 and r('score')+r('score',1)*256==score,'Episode transition retains accumulated points')
  end
 end
 check(r('remix_unlocked')==1 and row(14):find('DOS EPISODIOS PUBLICADOS',1,true)~=nil,'Full campaign has its own finale and unlocks Remix')
 shot('mesen-episode2-ending');press('a')
 check(r('episode')==0 and r('remix')==1 and r('completed')==0,'Remix begins again at the first episode')
 report:close();emu.stop(0)
end)
local total=0
emu.addEventCallback(function()
 total=total+1
 if total>48000 then report:write('FAIL timeout\n');report:close();emu.stop(2);return end
 local ok,err=coroutine.resume(runner)
 if not ok then report:write('FAIL '..tostring(err)..'\n');report:close();emu.stop(1);return end
 local controller={a=false,b=false,start=false,select=false,up=false,down=false,left=false,right=false}
 for name,value in pairs(input)do controller[name]=value end
 emu.setInput(controller,0)
end,emu.eventType.inputPolled)
