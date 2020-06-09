
%% Save master model
structGMM = masterGMM;    
save('Models/masterGMM.mat','structGMM');
saveGMM('Models/masterGMM.mat','Models/masterGMM.txt');
clear structGMM;

%% Save slave model
structGMM = slaveGMM;
save('Models/slaveGMM.mat','structGMM'); 
saveGMM('Models/slaveGMM.mat','Models/slaveGMM.txt');
clear structGMM;

%% Save coupling model
structGMM = cplGMM; 
save('Models/cplGMM.mat','structGMM');
saveGMM('Models/cplGMM.mat','Models/cplGMM.txt');
clear structGMM;
