clear;clc;

for i = 0:1:201
    disp(i)
    PNG = imread(['E:\mytest\All\IM',num2str(i),'.png']);
    PicPNG = rgb2gray(PNG);
    PixelNum = 0; AddX = 0; AddY = 0;

    for m = 1:1:512
        for n = 1:1:512
            if(PicPNG(m,n)~=0 && PicPNG(m,n)~=255)
                AddX = AddX + m;
                AddY = AddY + n;
                PixelNum = PixelNum + 1;
            end
        end
    end

    deltaX = 256-round(AddX*1.0/PixelNum);
    deltaY = 256-round(AddY*1.0/PixelNum);
    %======================================================
    Dicom = dicomread(['E:\mytest\All\IM',num2str(i)]);
    PNG2 = uint8(zeros(512,512,3));
    Dicom2 = uint16(zeros(512,512));

    for m = 1:1:512
        for n = 1:1:512
            if( (m-deltaX)<=0||(n-deltaY)<=0||(m-deltaX)>512||(n-deltaY)>512)
                PNG2(m,n,1) = PNG(5,5,1);PNG2(m,n,2) = PNG(5,5,2);PNG2(m,n,3) = PNG(5,5,3);
                Dicom2(m,n) = 0;
            else
                PNG2(m,n,1) = PNG(m-deltaX,n-deltaY,1);PNG2(m,n,2) = PNG(m-deltaX,n-deltaY,2);
                PNG2(m,n,3) = PNG(m-deltaX,n-deltaY,3);
                Dicom2(m,n) = Dicom(m-deltaX,n-deltaY);
            end
        end
    end

    imwrite(PNG2,['E:\mytest\ALL2\IM',num2str(i),'.png']);
    dicomwrite(Dicom2,['E:\mytest\ALL2\IM',num2str(i)])
end
