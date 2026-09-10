-- Independent Mesen campaign run: Estefania -> Chucho -> Daniel.
local root=PROJECT_ROOT
local labels={}
for line in io.lines(root..'build/el-cuartico.lbl') do
 local addr,name=line:match('al (%x+) %.(_[%w_]+)')
 if addr then labels[name]=tonumber(addr,16) end
end
local report=assert(io.open(root..'build/mesen-campaign-tests.txt','w'))
local function read(name,offset)return emu.read(assert(labels['_'..name])+ (offset or 0),emu.memType.nesDebug)end
local function check(ok,msg)
 report:write((ok and 'PASS ' or 'FAIL ')..msg..'\n');report:flush()
 if not ok then report:close();emu.stop(1) end
end
local function shot(name)
 local f=assert(io.open(root..'build/'..name..'.png','wb'));f:write(emu.takeScreenshot());f:close()
end
local f=0
local order={1,0,2}
local index=1
local menu_wait=90
local end_wait=0
local result_mask=0
local result_wait=0
local pics={}
local search_age=0
local search_round=-1
local function toward(input,x,y)
 local px,py=read('px'),read('py')
 if math.abs(px-x)>2 then input[px<x and 'right' or 'left']=true
 elseif math.abs(py-y)>2 then input[py<y and 'down' or 'up']=true
 else return true end
 return false
end
local function repair(input)
 if read('task_active')==1 then
  local t,p=read('repair_task'),read('task_progress')
  local tap=f%4<2
  if t==0 then
   local wanted=0
   for i=0,2 do if read('task_order',i)==p then wanted=i end end
   if read('task_cursor')~=wanted then input.down=tap else input.a=tap end
  elseif t==1 then
   local v,w=read('task_value'),read('task_target')
   if v~=w then input[v<w and 'right' or 'left']=true else input.a=tap end
  elseif t==2 then input.a=math.abs(read('task_value')-read('task_target'))<=3 and tap
  elseif read('task_phase')==1 then input[({'left','right','up','down'})[read('task_code',p)+1]]=tap end
  return
 end
 local px,py=read('px'),read('py');local t=nil
 for i=0,3 do if read('alarm',i)>0 and (t==nil or read('alarm',i)<read('alarm',t)) then t=i end end
 if t~=nil then
  local x=t%2==0 and 32 or 208;local y=t<2 and 64 or 136
  if py<140 and ((px<128)~=(x<128)) then toward(input,px<128 and 32 or 208,144)
  elseif toward(input,x,y) then input.a=f%4<2 end
 end
 if (input.left or input.right or input.up or input.down) and read('cooldown')==0 then input.b=true end
end
emu.addEventCallback(function()
 f=f+1
 if f>14000 then check(false,'timeout');emu.stop(2);return end
 local input={a=false,b=false,start=false,select=false,up=false,down=false,left=false,right=false}
 local mode=read('mode')
 if mode==3 and read('hud_on')==1 and search_round==read('round_no') then search_age=search_age+1
 else search_age=0;search_round=read('round_no') end
 if menu_wait>0 then menu_wait=menu_wait-1
 elseif mode==0 then
  if not pics.hub then shot('mesen-hub');pics.hub=true;check(read('completed')==0,'Free character choice at boot') end
  if read('host')~=order[index] then input.right=true;menu_wait=20
  else input.start=true;menu_wait=25 end
 elseif mode==7 then
  if not pics.intro then
   check(read('ex_on')==2,'Daniel intro uses static MMC5 extended attributes')
   shot('mesen-dany-intro');pics.intro=true
  end
  input.a=true;menu_wait=25
 elseif mode>=1 and mode<=3 and read('hud_on')==1 then
  if mode==1 then
   repair(input)
   if read('repairs')==3 and not pics.chucho then shot('mesen-chucho');pics.chucho=true end
  elseif mode==2 then
   if read('cue_wait')==0 then
    if read('cue_demo')==1 then input.a=true
    elseif read('cue_x')>=54 and read('cue_x')<=70 then input[({'a','b','left','right','up','down'})[read('cue_key')+1]]=true end
   end
   if read('hits')==5 and not pics.estefania then shot('mesen-estefania');pics.estefania=true end
   if read('rhythm_chain')==5 and not pics.streak then
    local points=read('attempt_score')+256*read('attempt_score',1)
    check(points==read('hits')*100+read('perfects')*50+100,'Five-note streak awards the exact bonus in Mesen')
    check(read('cheer')>0,'Streak celebration is active');pics.streak=true
   end
  elseif read('search_wait')==0 and read('feedback')==0 and search_age>=30 then
   local d,w=read('district'),read('target_district')
   if d~=w then
    if d%2~=w%2 then input[d%2<w%2 and 'right' or 'left']=true
    else input[d<w and 'down' or 'up']=true end
   else
   local t=read('target')
   local x,y=read('npc_x',t),read('npc_y',t)+4
   if read('cursor_x')<x then input.right=true
   elseif read('cursor_x')>x then input.left=true
   elseif read('cursor_y')<y then input.down=true
   elseif read('cursor_y')>y then input.up=true
   else
    if read('zoom_npc')~=t then input.b=true
    else
     local mark='lens'..read('round_no')
     if not pics[mark] then check(read('hover_npc')==t,'Lens and A share the selected person in round '..read('round_no'));pics[mark]=true end
     if read('round_no')==0 and not (read('seconds')==1 and read('tick')==59) then input.b=true
     else input.a=true end
    end
   end
   end
   if read('round_no')==1 and not pics.lastsecond then
    check(read('found')==1 and read('seconds')>=84,'Last-frame selection advances to a fresh round in Mesen');pics.lastsecond=true
   end
   if read('round_no')==2 and not pics.daniel then shot('mesen-daniel');pics.daniel=true end
  end
 elseif mode==4 and result_mask~=read('completed') then
  result_wait=result_wait+1
  if result_wait==20 then
   check(read('last_win')==1,'Completed game '..order[index])
   check(read('result_grade')==3,'Clean run earns three result medals')
   check(read('completed')~=7,'Ending remains locked with unfinished games')
   result_mask=read('completed');index=index+1;result_wait=0;input.start=true;menu_wait=25
  end
 elseif mode==4 and read('last_win')==0 then check(false,'unexpected loss');emu.stop(3)
 elseif mode==5 then
  end_wait=end_wait+1
  if end_wait==25 then
   check(read('completed')==7,'All three stamps unlock ending in a non-default order')
   check(read('found')==3,'Daniel completed three searches')
   shot('mesen-ending');report:write('ALL MESEN CAMPAIGN CHECKS PASSED\n');report:close();emu.stop(0)
  end
 end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
