function [pdata, odata, odata_dyn, otarget] = cds_load_data()

% Loading raw data

% Initialize variables
pdata={};               % Position data
odata={};               % Orientation data
odata_dyn={};           % Orientation dynamics
count=1;                % Index
otarget = zeros(4,1);   % Target in orientation (The target for position will be 0,0,0)

file_ind = [1 12 6 4 2 3]; % Indexes of the demonstrations to be used in learning

for i = file_ind
    x = load(sprintf('data/ppdata/s1_pos_%0.3d.txt',i)); % It loads a file with 7 columns (3D position + orientation as axis angles)
    x = x(1:10:end-500,:); %downsampling by 10
    for j=1:size(x,2)
        x(:,j)=smooth(x(:,j),100);
    end
    
    otarget = otarget + x(end,4:7)';      % Setting the target of the orientation as the last point of the demonstrations
    odata{count} = x(:,4:7)';             % Separating orientation data
    disp(x(end,:));                       % The last element of x
    x = x - repmat(x(end,:),size(x,1),1); % Substracting the last value from all elements of x
                                          % Now the values in x should decrease nicely to zero. Note that SEDS will
                                          % add a (0, 0, 0) to the end of each demonstration (which corresponds to
                                          % zero velocity at the end of each demo), but if it doesn't decrease nicely
                                          % it will affect the dynamics by being a too sudden change. Can cause
                                          % overshooting the attractor. It happens frequently in learning from
                                          % segmented data if not every part of the demonstration ended with zero
                                          % velocity.
    
    % Plot demonstration data - 3D Position
    figure(1)
    plot3(x(:,1),x(:,2),x(:,3),'*');
    figure(2)
    nrmx=sqrt(sum(x(:,1:3).^2,2));
    subplot(3,1,1); hold on; plot(nrmx);         ylabel('Norm of position');
    subplot(3,1,2); hold on; plot(x(:,4:7),'.'); ylabel('Orient_dyn');
    subplot(3,1,3); hold on; plot(x(:,1:3),'.'); ylabel('Pos_dyn');
    pdata{count} = x(:,1:3)';             % Should be called pdata_dyn
    odata_dyn{count} = x(:,4:7)';
    count=count+1;
end

otarget = otarget/length(file_ind);      % The target orientation is the average target from all the demonstrations
figure(1)
axis equal
axis tight

end