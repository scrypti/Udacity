grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost):
    openlist = [[0, init[0], init[1]]]  # [g-value, x, y]
    visited = [[0 for i in range(6)] for j in range(5)]
    visited[0][0] = 1  # visited  = [init]

    def find_cheapest_index(l):
        i = 0
        for j in range(1, len(l)):
            if l[i][0] > l[j][0]:
                i = j
        return i

    def explore(node, visited, grid):
        list = []
        x = node[1]
        y = node[2]
        g = node[0]  # g-value: how many steps did it take to get there (previous +1)

        x_bound = len(grid) - 1
        y_bound = len(grid[0]) - 1
        for i in range(len(visited)):
            for j in range(len(delta)):
                # if valid move -> add to list
                x_ = x + delta[j][0]
                y_ = y + delta[j][1]

                # out of bounds check
                if (x_ < 0) or (y_ < 0) or (x_ > x_bound) or (y_ > y_bound):
                    # print('out of bounds: ', x_, ' ', y_)
                    continue

                # is wall
                if grid[x_][y_] is 1:
                    continue

                # already visited check
                if [x_, y_] in visited:
                    # print('already visited: ', x_, ' ', y_)
                    continue

                list.append([g + 1, x_, y_])
        return list

    while len(openlist) > 0:

        # take cheapest item from list
        cheapest_index = find_cheapest_index(openlist)
        node = openlist[cheapest_index]
        openlist.pop(cheapest_index)
        visited[node[1]][node[2]] = 1  # visited.append([node[1], node[2]])

        if visited[goal[0]][goal[1]] is 1:  # if goal in visited:
            return node

        # explore from current coordinate
        nodes = explore(node, visited, grid)
        for node in nodes:
            if node not in openlist:
                openlist.append(node)
        # print('openlist: ', openlist)
    print("search failed")

print(search(grid, init, goal, cost))

print(grid)

visited = [[0 for i in range(6)] for j in range(5)]

print(visited)
