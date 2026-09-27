-- Independent whole-ROM replay of a controller-only FCEUmm playthrough.
-- No emulated RAM, CPU registers or save states are written.
local root=PROJECT_ROOT
local labels={}
for line in io.lines(root..'build/el-cuartico.lbl') do
 local addr,name=line:match('al (%x+) %.(_[%w_]+)')
 if addr then labels[name]=tonumber(addr,16) end
end
local function r(name,i)return emu.read(labels['_'..name]+(i or 0),emu.memType.nesDebug)end
local trace={}
for line in io.lines(root..'build/adventure-inputs.txt') do
 local n,m=line:match('(%d+) (%d+)');trace[#trace+1]={tonumber(n),tonumber(m)}
end
local report=assert(io.open(root..'build/mesen-adventure-tests.txt','w'))
local function check(ok,label)
 report:write((ok and 'PASS ' or 'FAIL ')..label..'\n');report:flush()
 if not ok then emu.stop(1) end
end
local index,remaining,frame=1,trace[1][1],0
local names={[0]='b',[2]='select',[3]='start',[4]='up',[5]='down',[6]='left',[7]='right',[8]='a'}
local seen={}
emu.addEventCallback(function()
 frame=frame+1
 if r('mode')==10 and r('adv_command')==10 and r('adv_ui_page')==20 then
  seen[r('adv')..':'..r('adv',1)]=true
 end
 if index>#trace then
  check(r('adv_save',4)+256*r('adv_save',5)==511,'All nine stages complete in independent Mesen replay')
  check(r('adv_save',3)==255,'All eight tapes collected in Mesen')
  check(r('adv_save',2)==7,'All three classic rehearsals complete in Mesen')
  local count=0;for _ in pairs(seen) do count=count+1 end
  check(count==66,'All 66 rooms were actually entered')
  check(r('adv_ui_page')==1,'Ending returns to the studio without a softlock')
  report:close();emu.stop(0);return
 end
 local mask=trace[index][2];local input={}
 for bit,name in pairs(names) do input[name]=math.floor(mask/2^bit)%2==1 end
 emu.setInput(input,0)
 remaining=remaining-1
 if remaining==0 then index=index+1;if trace[index] then remaining=trace[index][1] end end
end,emu.eventType.inputPolled)
