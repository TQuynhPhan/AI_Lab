function readDataset(fileName)
    attrNames=[]
    df=[]
    open(fileName) do f
        fir=readline(f)
        for i in split(fir,",")
            push!(attrNames,i)
        end
        for line in readlines(f)
            element=Dict()
            cnt=1
            for i in split(line,",")
                if i=="Iris-setosa"||i=="Iris-versicolor"||i=="Iris-virginica"
                    push!(element,attrNames[cnt]=>i)
                else
                    push!(element,attrNames[cnt]=>parse(Float64,i))
                cnt+=1
                end
            end
            push!(df,element)
        end
    end
    return df
end


MAX_TREE_DEPTH=3
MIN_SAMPLE_SIZE=4
mutable struct Node
    dataset::Vector 
    isLeaf::Bool
    cutoff::Float64
    cutoffAttr::String
    attrNames::Vector
    attrValues::Dict
    leftNode::Union{Node,Nothing}
    rightNode::Union{Node,Nothing}
    predict::String
    depth::Int64
end


function buildNode(node)
    if node.depth<MAX_TREE_DEPTH && length(node.dataset)>=MIN_SAMPLE_SIZE && length(Set([elem["class"] for elem in node.dataset]))>1
        maxIg,attribute,cutoff=maxInformationGain(node.dataset,node.attrNames,node.attrValues)
        
        if maxIg>0
            node.cutoff=cutoff
            node.cutoffAttr=attribute
            
            left=[i for i in node.dataset if i[attribute]<cutoff]
            right=[i for i in node.dataset if i[attribute]>=cutoff]
            node.leftNode=Node(left,false,0.0,"",node.attrNames,node.attrValues,nothing,nothing,"",node.depth+1)
            buildNode(node.leftNode)
            node.rightNode=Node(right,false,0.0,"",node.attrNames,node.attrValues,nothing,nothing,"",node.depth+1)
            buildNode(node.rightNode)
        else
            node.isLeaf=true
        end
    else
        node.isLeaf=true
    end

    if node.isLeaf==true
        seCount=verCount=virCount=0
        seCount=count(i->(i=="Iris-setosa"),elem["class"] for elem in node.dataset)
        verCount=count(i->(i=="Iris-versicolor"),elem["class"] for elem in node.dataset)
        virCount=count(i->(i=="Iris-virginica"),elem["class"] for elem in node.dataset)

        domClass="Iris-setosa"
        domCount=seCount
        if verCount>=domCount
            domClass="Iris-versicolor"
            domCount=verCount
        end
        if virCount>=domCount
            domClass="Iris-virginica"
            domCount=virCount
        end
        node.predict=domClass
        
    end  
end


function predictNode(node,sample)
    if node.isLeaf==true
        return node.predict
    else
        if sample[node.cutoffAttr]<node.cutoff
            return predictNode(node.leftNode,sample)
        else
            return predictNode(node.rightNode,sample)
        end
    end
end


function buildTree(df, attrNames,attrValues)
    root=Node(df,false,0.0,"",attrNames,attrValues,nothing,nothing,"",0)
    buildNode(root)
    return root
end


function entropy(df)
    entropy=0
    name="class"
    values=["Iris-setosa","Iris-versicolor","Iris-virginica"]
    for val in values
        p=length([i for i in df if i[name]==val])/length(df)
        if p>0
            entropy-=p*log2(p)
        end
    end
    return entropy     
end


function informationGain(df, attrName, cutoff)
    
    arrSmaller=[i for i in df if i[attrName]<cutoff]
    pSmaller=length(arrSmaller)/length(df)
    
    arrGreaterEqual=[i for i in df if i[attrName]>=cutoff]
    pGreaterEqual=length(arrGreaterEqual)/length(df)
    
    infoGain=entropy(df) 
    infoGain-=pSmaller*entropy(arrSmaller)+pGreaterEqual*entropy(arrGreaterEqual)
     
    return infoGain
end


function maxInformationGain(df, attrNames, attrValues)
    max=0 
    maxAttr=""
    maxVal=0
    for i in attrNames
        for j in attrValues[i] 
            ig=informationGain(df,i,j)
            if ig>=max
                max=ig
                maxAttr=i
                maxVal=j
            end
        end
    end
    return max,maxAttr,maxVal
end


function calcAccuracy(root,df)
    accuracy=0
    for i in df
        if i["class"]==predictNode(root,i)
            accuracy+=1
        end
    end
    return accuracy/length(df)
end





df=readDataset("iris.csv")

n=length(df)
println("Dataset length: ",n)
m=trunc(Int,(2/3)*n)

using Random
Random.seed!(1234)
randNum=unique([rand(1:n) for r in 1:(2*m)])[1:m]

train=df[randNum]
println("Training length: ",length(train))

test=[]
for i in range(1,length(df))
    if i ∉ randNum
        push!(test,df[i])
    end
end
println("Test length: ",length(test))

attrValues=Dict()

for attr in keys(df[1]) 
    val=Set()
    for s in df
        push!(val,s[attr])
    end
    attrValues[attr]=val
end

attrNames=["sepal_length", "sepal_width", "petal_length", "petal_width"]
root=buildTree(df,attrNames,attrValues)
println("Accuracy: ",calcAccuracy(root,test))