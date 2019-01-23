print("--------------------")

## Load node layer
node_layer = QgsProject.instance().mapLayersByName('node')[0]
## Create node list
same_node = []
differ_node = []
wrong_node = []
## Classify node
for f in node_layer.getFeatures() :
    if (f['NUM_LINK'] == 0) :
        same_node.append([f['MESH_ID'], f['NODE_ID']])
    else :
        if [f['MESH_ID'], f['NODE_ID']] == [f['ADJMAP_ID'], f['ADJND_ID']] :
            wrong_node.append([f['MESH_ID'], f['NODE_ID']])
        else :
            differ_node.append([f['MESH_ID'], f['NODE_ID'], f['ADJMAP_ID'], f['ADJND_ID']])

print(len(same_node))
print(len(differ_node))
print(len(wrong_node))

## fix node
for i in differ_node :
    if i[2:] in wrong_node :
        differ_node.append([i[2],i[3], i[0], i[1]])

## Delete overlapped node
diff_node = []
for i in differ_node :
    if i[2:] + i[:2] in diff_node :
        print('skip')
    else :
        diff_node.append(i)

## Load pedestrian road layer
line_layer = QgsProject.instance().mapLayersByName('road')[0]
line_layer.startEditing()
error_node_list = []

### merge in same_node
for n in same_node :
    ## Get Features
    req_B = line_layer.selectByExpression('"MESH_ID"=' + str(n[0]) + ' and ' + '"S_NODE_ID"=' + str(n[1]) + ' and ' + '"LINK_FACIL"=2')
    Feature_B = line_layer.selectedFeatures()
    req_A = line_layer.selectByExpression('"MESH_ID"=' + str(n[0]) + ' and ' + '"E_NODE_ID"=' + str(n[1]) + ' and ' + '"LINK_FACIL"=2')
    Feature_A = line_layer.selectedFeatures()
    
    ## Classify Features
    # case 1
    if (len(Feature_B) == 1) and (len(Feature_A) == 1) :
        line_B = Feature_B[0]
        line_A = Feature_A[0]
    # case 2
    elif (len(Feature_B) == 2) and (len(Feature_A) == 0) :
        line_B = Feature_B[0]
        line_A = Feature_B[1]
    # case 3
    elif (len(Feature_A) == 2) and (len(Feature_B) == 0) :
        line_B = Feature_A[0]
        line_A = Feature_A[1]
    # case 4
    else :
        error_node_list.append(n)
        print("--------Error!------")
        continue

    #Get line B end point
    B_end = line_B[3]
    
    #Get line B id
    id_B = line_B.id()
    
    #Tranform line B geometry
    geom_B = line_B.geometry()
    
    #Extract line B wkt point
    node_B = geom_B.asWkt()[18:-2].split(', ')
    B_first = node_B[0]
    B_last = node_B[-1]

    #Get line A id
    id_A = line_A.id()
    
    #Tranform line A geometry
    geom_A = line_A.geometry()
    
    #Extract line A wkt point
    node_A = geom_A.asWkt()[18:-2].split(', ')
    A_first = node_A[0]
    A_last = node_A[-1]

    ## Create new wkt
    if A_first == B_first :
        new_wkt_list = node_A[-1:0:-1] + node_B
    elif A_first == B_last :
        new_wkt_list = node_B + node_A[1:]
    elif A_last == B_first :
        new_wkt_list = node_A + node_B[1:]
    elif A_last == B_last :
        new_wkt_list = node_A[:-1] + node_B[-1::-1]

    ##Convert X,Y
    new_line = []
    for point in new_wkt_list :
        x = float(point.split(' ')[0])
        y = float(point.split(' ')[1])
        #x = float(point[0:23])
        #y = float(point[25:-1])
        xy = QgsPoint(x, y)
        new_line.append(xy)

    ##change line A geometry
    new_geom = QgsGeometry.fromPolyline(new_line)
    
    # print(new_geom)
    line_layer.dataProvider().changeGeometryValues({id_A : new_geom})
    
    ##Update end point attribute
    line_layer.changeAttributeValue(id_A, 3, B_end)
    line_layer.updateFields()
    
    ## delete line
    line_layer.dataProvider().deleteFeatures([id_B])

## Merge in different node
for n in diff_node :
    ## Get features
    req_B = line_layer.selectByExpression('"MESH_ID"=' + str(n[0]) + ' and ' + '"S_NODE_ID"=' + str(n[1]) + ' and ' + '"LINK_FACIL"=2')
    Feature_B = line_layer.selectedFeatures()
    if len(Feature_B) == 0 :
        req_B = line_layer.selectByExpression('"MESH_ID"=' + str(n[0]) + ' and ' + '"E_NODE_ID"=' + str(n[1]) + ' and ' + '"LINK_FACIL"=2')
        Feature_B = line_layer.selectedFeatures()
        if len(Feature_B) == 0 :
            continue
        else :
            error_node_list.apeend(n)

    req_A = line_layer.selectByExpression('"MESH_ID"=' + str(n[2]) + ' and ' + '"S_NODE_ID"=' + str(n[3]) + ' and ' + '"LINK_FACIL"=2')
    Feature_A = line_layer.selectedFeatures()
    if len(Feature_A) == 0 :
        req_A = line_layer.selectByExpression('"MESH_ID"=' + str(n[2]) + ' and ' + '"E_NODE_ID"=' + str(n[3]) + ' and ' + '"LINK_FACIL"=2')
        Feature_A = line_layer.selectedFeatures()
        if len(Feature_A) == 0 :
            continue
        else :
            error_node_list.apeend(n)

    ## Classify Features
    # case 1
    if (len(Feature_B) == 1) and (len(Feature_A) == 1) :
        line_B = Feature_B[0]
        line_A = Feature_A[0]
    # case 2
    elif (len(Feature_B) == 2) and (len(Feature_A) == 0) :
        line_B = Feature_B[0]
        line_A = Feature_B[1]
    # case 3
    elif (len(Feature_A) == 2) and (len(Feature_B) == 0) :
        line_B = Feature_A[0]
        line_A = Feature_A[1]
    # case 4
    else :
        error_node_list.append(n)
        print("--------Error!------")
        continue

    #Get line B end point
    B_end = line_B[3]
    
    #Get line B id
    id_B = line_B.id()
    
    #Tranform line B geometry
    geom_B = line_B.geometry()
    
    #Extract line B wkt point
    node_B = geom_B.asWkt()[18:-2].split(', ')
    B_first = node_B[0]
    B_last = node_B[-1]

    #Get line A id
    id_A = line_A.id()
    
    #Tranform line A geometry
    geom_A = line_A.geometry()
    
    #Extract line A wkt point
    node_A = geom_A.asWkt()[18:-2].split(', ')
    A_first = node_A[0]
    A_last = node_A[-1]

    ## Create new wkt
    if A_first == B_first :
        new_wkt_list = node_A[-1:0:-1] + node_B
    elif A_first == B_last :
        new_wkt_list = node_B + node_A[1:]
    elif A_last == B_first :
        new_wkt_list = node_A + node_B[1:]
    elif A_last == B_last :
        new_wkt_list = node_A[:-1] + node_B[-1::-1]

    ##Convert X,Y
    new_line = []
    for point in new_wkt_list :
        x = float(point.split(' ')[0])
        y = float(point.split(' ')[1])
        #x = float(point[0:23])
        #y = float(point[25:-1])
        xy = QgsPoint(x, y)
        new_line.append(xy)

    ##change line A geometry
    new_geom = QgsGeometry.fromPolyline(new_line)
    line_layer.dataProvider().changeGeometryValues({id_A : new_geom})
    
    ##Update end point attribute
    line_layer.changeAttributeValue(id_A, 3, B_end)
    line_layer.updateFields()
    
    ## delete line
    line_layer.dataProvider().deleteFeatures([id_B])
