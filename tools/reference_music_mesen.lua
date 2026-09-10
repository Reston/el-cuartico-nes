-- Observe real APU writes. No memory writes, cheats or saved-state loading.
local root=PROJECT_ROOT
local labels={}
for line in io.lines(root..'build/el-cuartico.lbl')do
 local address,name=line:match('al (%x+) %.(_[%w_]+)')
 if address then labels[name]=tonumber(address,16)end
end
local report=assert(io.open(root..'build/mesen-reference-music-tests.txt','w'))
local function r(name)return emu.read(assert(labels['_'..name]),emu.memType.nesDebug)end
local function check(ok,label)
 report:write((ok and 'PASS ' or 'FAIL ')..label..'\n');report:flush()
 if not ok then error(label)end
end
local input={}
local function frames(n,keys)for _=1,n do input=keys or {};coroutine.yield()end end
local function press(key)frames(5,{[key]=true});frames(15)end
local registers,attacks,effects={},0,0
emu.addMemoryCallback(function(address,value)
 registers[address]=value
 if address==0x4003 then attacks=attacks+1 end
 if address==0x4004 then effects=effects+1 end
end,emu.callbackType.write,0x4000,0x400f)
local semitones={C=0,Cs=1,D=2,Ds=3,E=4,F=5,Fs=6,G=7,Gs=8,A=9,As=10,B=11}
local function midi(note)
 local letter,octave=note:match('^(%a+)(%d)$')
 return 12*(tonumber(octave)+1)+assert(semitones[letter])
end
local function period(note,triangle)
 return math.floor(1789773/((triangle and 32 or 16)*440*2^((midi(note)-69)/12))-1+.5)
end
local file=assert(io.open(root..'assets/song-arrangements.json','r'))
local document=file:read('*a');file:close()
local function score(id)
 local start=assert(document:find('"id": "'..id..'"',1,true))
 local following=document:find('"id":',start+6,true)
 local section=document:sub(start,following and following-1 or #document)
 local lead,trigger,bass,drum,volume={},{},{},{},{}
 local melody=assert(section:match('"lead_sixteenths"%s*:%s*(.-)"bass_quarters"'))
 for note,length in melody:gmatch('"(%w+)"%s*,%s*(%d+)')do
  for i=1,tonumber(length)do lead[#lead+1]=note;trigger[#trigger+1]=i==1 and note~='R'end
 end
 for note in assert(section:match('"bass_quarters"%s*:%s*%[(.-)%]')):gmatch('"(%w+)"')do bass[#bass+1]=note end
 for value in assert(section:match('"noise_periods"%s*:%s*%[(.-)%]')):gmatch('%d+')do drum[#drum+1]=tonumber(value)end
 for value in assert(section:match('"noise_volumes"%s*:%s*%[(.-)%]')):gmatch('%d+')do volume[#volume+1]=tonumber(value)end
 assert(#lead==64 and #bass==16 and #drum==16 and #volume==16)
 return {lead=lead,trigger=trigger,bass=bass,drum=drum,volume=volume}
end
local runner=coroutine.create(function()
 frames(90)
 for _,item in ipairs({{'menu',18},{'estefania',15}})do
  local id,tempo=item[1],item[2]
  if id=='estefania'then press('right');press('a');press('a')end
  local expected=score(id)
  for _=1,600 do if r('song_step')==0 and r('song_tick')==0 then break end;frames(1)end
  assert(r('song_step')==0 and r('song_tick')==0)
  local bad_pitch,bad_rest,bad_tie,bad_bass,bad_drum=0,0,0,0,0
  local effects_before=effects
  for _=1,tempo*32*2 do
   local tick,step=r('song_tick'),r('song_step')
   local half=math.floor(tempo/2)
   local sub=tick>=half and 1 or 0
   local index=step*2+sub+1
   local phase=tick-sub*half
   local note=expected.lead[index]
   local before=attacks
   frames(1)
   local actual=(registers[0x4002]or 0)+((registers[0x4003]or 0)%8)*256
   if note=='R'then
    if registers[0x4000]%16~=0 then bad_rest=bad_rest+1 end
   elseif actual~=period(note,false)then bad_pitch=bad_pitch+1 end
   local retrigger=(tick==0 or tick==half)and expected.trigger[index]
   if attacks-before~=(retrigger and 1 or 0)then bad_tie=bad_tie+1 end
   local bass_active=step%2==0 or tick<4
   local bass_period=(registers[0x400a]or 0)+((registers[0x400b]or 0)%8)*256
   if bass_active then
    if registers[0x4008]==0 or bass_period~=period(expected.bass[math.floor(index/4-.25)+1],true)then bad_bass=bad_bass+1 end
   elseif registers[0x4008]~=0 then bad_bass=bad_bass+1 end
   local drum_index=(index-1)%16+1
   if registers[0x400e]~=expected.drum[drum_index]or registers[0x400c]%16~=(phase<3 and expected.volume[drum_index]or 0)then bad_drum=bad_drum+1 end
  end
  check(bad_pitch==0,id..': every audible lead pitch matches the independent score-to-frequency calculation')
  check(bad_rest==0,id..': scored rests silence pulse one')
  check(bad_tie==0,id..': held notes preserve oscillator phase and new notes articulate on sixteenths')
  check(bad_bass==0,id..': triangle plays the arranged bass octave with the intended gate')
  check(bad_drum==0,id..': noise channel follows the complete sixteenth-note groove')
  check(effects==effects_before,id..': music leaves pulse two available for feedback')
 end
 -- Resume a sustained melody in the second half of an eighth note.
 for _=1,600 do
  if r('reference_pitch')~=0 and r('song_tick')==10 then break end
  frames(1)
 end
 press('start')
 local step,tick=r('song_step'),r('song_tick')
 frames(180)
 check(r('paused')==1 and r('song_step')==step and r('song_tick')==tick,'Pause freezes the reference phrase clock')
 check(registers[0x4000]%16==0 and registers[0x4004]%16==0 and registers[0x4008]==0 and registers[0x400c]%16==0,'Pause silences every music and feedback voice')
 frames(1,{start=true});frames(2)
 local index=r('song_step')*2+(r('song_tick')>=7 and 1 or 0)+1
 local note=score('estefania').lead[index]
 local actual=registers[0x4002]+registers[0x4003]%8*256
 check(r('paused')==0 and note~='R'and actual==period(note,false),'Resume restores the correct sustained reference pitch without restarting the phrase')
 report:close();emu.stop(0)
end)
local total=0
emu.addEventCallback(function()
 total=total+1
 if total>5000 then report:write('FAIL timeout\n');report:close();emu.stop(2);return end
 local ok,err=coroutine.resume(runner)
 if not ok then report:write('FAIL '..tostring(err)..'\n');report:close();emu.stop(1);return end
 local controller={a=false,b=false,start=false,select=false,up=false,down=false,left=false,right=false}
 for name,value in pairs(input)do controller[name]=value end
 emu.setInput(controller,0)
end,emu.eventType.inputPolled)
