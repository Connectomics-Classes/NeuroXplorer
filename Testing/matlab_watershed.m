% setup server and token
cajal3d;
oo = OCP();
oo.setImageToken('kasthuri11cc');
oo.setAnnoToken('cv_kasthuri11_membrane_2014');
q = OCPQuery;
q.setType(eOCPQueryType.probDense);
% you want this q.setCutoutArgs([4400,5424],[5440,6464],[1100,1200],1);
q.setCutoutArgs([4400,5424],[5440,6464],[1100,1105],1); %testing
M = oo.query(q);
image(M)

% get image data
q.setType(eOCPQueryType.imageDense);
IM = oo.query(q);

% threshold for viewing
M2 = RAMONVolume; M2.setCutout(M.data > 0.7);
h = image(IM); 
h.associate(M2);

% watershed
S = segmentWatershed2D(M,10,5,10);
h = image(IM); h.associate(S)