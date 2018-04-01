clear;
close all;
clc;

Nimages = 30;
noOfFeatures = 2;
trackedPoints = zeros(Nimages,2,noOfFeatures);
lastParameters = zeros(noOfFeatures,6);
lastPoints = zeros(2,noOfFeatures);

reSurf = 15;

for i = 1:Nimages
    if rem(i,reSurf)==1
        % Storing templates
        image0 = imread(strcat('../input/',num2str(i),'.jpg'));
        templatePoints = surf_points(image0,noOfFeatures); % Second is bigger
        trackedPoints(i,:,:) = transpose(templatePoints);
        templates = zeros(noOfFeatures,41,41);

        for ii = 1:noOfFeatures
            templates(ii,:,:) = image0(templatePoints(ii,1)-20:templatePoints(ii,1)+20,templatePoints(ii,2)-20:templatePoints(ii,2)+20); %CHECK
            lastParameters(ii,:) = [1,0,0,0,1,0];
            lastPoints = trackedPoints(i,:,:);
            lastPoints = reshape(lastPoints,[2,noOfFeatures]);
        end
    else
        image = imread(strcat('../input/',num2str(i),'.jpg'));
        [imgradX,imgradY] = imgradientxy(image);

        for j = 1:noOfFeatures
            for kkkk = 1:3
                deltaP = zeros(1,6);
                currStrucTen = findstructen(image,round(lastPoints(:,j)),imgradX,imgradY);
                for a1 = 1:41
                    for a2 = 1:41
                        % CHECK in case of mistake
                        rownum = round(lastPoints(1,j))+a1-20;  
                        colnum = round(lastPoints(2,j))+a2-20;
                        currI = interp2(image,rownum,colnum);
                        % transpose(double([imgradX(currX,currY),imgradY(currX,currY)])) 
                        % [[currX,currY,1,0,0,0]; [0,0,0,currX,currY,1]]
                        current = double([imgradX(rownum,colnum),imgradY(rownum,colnum)]) * [[colnum,rownum,1,0,0,0]; [0,0,0,colnum,rownum,1]];
                        temp = double(templates(j,a1,a2) - currI) * current;
                        deltaP = temp + deltaP;
                    end
                    % deltaP
                end
                origrow = (trackedPoints(i-rem(i-1,reSurf),1,j));
                origcol = (trackedPoints(i-rem(i-1,reSurf),2,j));
                alpha = deltaP;
                beta = eye(6)/currStrucTen;
                deltaP = deltaP / currStrucTen;
                lastParameters(j,:) = lastParameters(j,:) + deltaP;
                affine = transpose(reshape(deltaP,[3,2]));
                lastPoints(:,j)  =  lastPoints(:,j) + affine * [origrow;origcol;1];
                lastPoints(:,j);
            end
        end
        trackedPoints(i,:,:) = lastPoints;
    end
    i
end


%%% Save all the trajectories frame by frame
% variable trackedPoints assumes that you have an array of size 
% No of frames * 2(x, y) * No Of Features
% noOfFeatures is the number of features you are tracking
% Frames is array of all the frames(assumes grayscale)
noOfPoints = 1;
for i=1:Nimages
    NextFrame = imread(strcat('../input/',num2str(i),'.jpg'));
    imshow(uint8(NextFrame)); hold on;
    for nF = 1:noOfFeatures
        plot(trackedPoints(1:noOfPoints, 1, nF), trackedPoints(1:noOfPoints, 2, nF),'*')
    end
    hold off;
    saveas(gcf,strcat('../output2/',num2str(i),'.jpg'));
    close all;
    noOfPoints = noOfPoints + 1;
end