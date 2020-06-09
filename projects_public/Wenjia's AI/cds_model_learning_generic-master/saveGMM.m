function saveGMM(inpath, outpath)

if(isempty(inpath))
   [FileName,PathName] = uigetfile('*.mat','Input GMM .mat file');
   inpath = [PathName FileName];
end
if(isempty(outpath))
     [FileName,PathName] = uiputfile('*.gmm','Output file');
   outpath = [PathName FileName];
end
if(ischar(inpath))
    load(inpath);
else
    structGMM = inpath;
end

output = fopen(outpath,'w');

fprintf(output, '%f\n', length(structGMM.Priors));


fprintf(output, '%d\n', size(structGMM.Mu,1));


fprintf(output, '\n');
for i=1:length(structGMM.Priors)
    fprintf(output, '%f\t', structGMM.Priors(i));
end
fprintf(output, '\n');


fprintf(output, '\n');
for i=1:size(structGMM.Mu,1)
    for j=1:size(structGMM.Mu,2)
    fprintf(output, '%f\t', structGMM.Mu(i,j));
    end
    fprintf(output, '\n');
end
fprintf(output, '\n');

fprintf(output, '\n');
for i=1:size(structGMM.Sigma,3)
    for j=1:size(structGMM.Sigma,1)
        for k=1:size(structGMM.Sigma,2)
            fprintf(output, '%f\t', structGMM.Sigma(j,k,i));
        end
    fprintf(output, '\n');
    end
    fprintf(output, '\n');
end
fprintf(output, '\n');

