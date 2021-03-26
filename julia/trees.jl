# Computing polymorphisms of small oriented trees

using DelimitedFiles
#using Iterators

function read_graphs(path)
    # in: {path} -- path to a file with graphs in Nauty's simple format (nv ne edges)
    # out: {graphs} -- a 2D array, one graph per line
    graphs = convert(Array{Int}, readdlm(path))
    graphs = [tuple(graphs[i,:]...) for i in 1:size(graphs, 1)]    
    return graphs
end


function compute_levels(tree)
    nv = tree[1]
    ne = tree[2]    
    levels = zeros(Int, nv)
    done = zeros(Bool, nv)
    done[0+1] = true # start with vertex 0
    closed = false
    while !closed
        closed = true
        for i in 1:ne
            u, v = tree[2i+1], tree[2i+2]
            if done[u+1] & !done[v+1]
                closed = false
                levels[v+1] = levels[u+1] + 1
                done[v+1] = true
            elseif done[v+1] & !done[u+1]
                closed = false
                levels[u+1] = levels[v+1] - 1
                done[u+1] = true
            end
        end
    end
    levels = levels .- minimum(levels)
    height = maximum(levels)
    return height, levels
end


function is_core(tree)
    nv, ne = tree[1], tree[2]
    height, levels = compute_levels(tree)
    if height <= 3
        return false
    else
        #todo implement exhaustive search
        # DFS on edges_per_level to edges_per_level, remember if nonsurjective
        # product = Iterators.product([0:nv-1 for i in 1:nv]...)
        # for t in product
        #     println(t)
        # end
        # return false
    end

end

function main()
    trees = read_graphs("./test/all_triads9.trees")
    trees = trees[1:1]
    for tree in trees        
        if is_core(tree)
            println(tree)
        end
    end
end


main()