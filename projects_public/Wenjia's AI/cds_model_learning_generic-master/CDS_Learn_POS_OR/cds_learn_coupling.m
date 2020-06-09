function [cplGMM] = cds_learn_coupling(pdata, odata, odata_dyn)
%CDS_LEARN_COUPLING learns a GMM representation for the coupling function

%% Learn Model
% We always assume a 2D coupling function given by the 
% ==> norm in x-y axes combined with z coordinate
cplfnc = @(x)([sum(x(1:2,:).^2,1);x(3,:)]); 

cpldata=[];
for i=1:length(odata)
    cpldata = [cpldata, [pdata{i}; odata_dyn{i}]];
end

cplGMM = learn_coupling(cpldata, 1:3, 4:7, cplfnc, 8);

%% Test model 
% Loading a demo for testing the coupling model
x=load(sprintf('data/ppdata/s1_pos_%0.3d.txt',6));     % ==> Demonstration 6 for testing
x(:,1:3) = x(:,1:3) - repmat(x(end,1:3),size(x,1),1);
 
% Calculating coupling output using the loaded demo
or=GMR(cplGMM.Priors, cplGMM.Mu, cplGMM.Sigma, cplfnc(x(:,1:3)'), 1:cplGMM.coupl_dim,cplGMM.coupl_dim+1:size(cplGMM.Mu,1));

%% Plotting
figure(2)
subplot(2,1,2);
hold on
plot(or','-','Linewidth',4);

end

