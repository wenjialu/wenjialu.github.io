function [ ] = ppPosOrient( nrdem )
% Preprocess raw demonstration data: smoothing and converting to position
% and axis-angle orientation. We asume the same file format as in the EPFL
% data recordings.


for i = 1:nrdem
        disp(i);
        sfile_in = sprintf('rawdata/s1_data_%0.3d.txt',i); % Each row in this file is the serialized homogeneous transformation matrix
        data = load(sfile_in);
        
        for j = 1:size(data,1)
            temp = [vec2mat(data(j,1:12), 4); 0 0 0 1];
            data_pos_aa(j,:) = [data(j,4) data(j,8) data(j,12) vrrotmat2vec(temp(1:3,1:3))];
        end
        
        for k = 1:size(data_pos_aa,2)
            data_pos_aa(:,k) = smooth(data_pos_aa(:,k),500);
        end
               
        sfile_out = sprintf('ppdata/s1_pos_%0.3d.txt',i); % Each row in this file contains the 3D position and the axis-angle representation of orientation
        save(sfile_out,'data_pos_aa','-ascii');
        
        clear data_pos_aa;       
    
end


end

