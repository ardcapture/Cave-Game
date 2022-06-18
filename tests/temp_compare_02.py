Second

def set_next_position_v02(self):
    random.shuffle(DIRECTIONS)
    poss_directions = []
    poss_position_List = []
    for d in DIRECTIONS:
        poss_position = (self.current_poistion_v02[0] + (
            d[0] * GRID_SIZE * 2), self.current_poistion_v02[1] + (d[1] * GRID_SIZE * 2))
        if poss_position in [obj.position for obj in self.objs]:
            if poss_position not in self.past_positions_v02:
                poss_position_List.append(poss_position)

    if len(poss_position_List) > 1:
        bias = [100, 100, 1, 1]
        randomResult = random.choices(poss_position_List, k=1, weights=bias[:len(poss_position_List)])
        result = randomResult[0]
    if len(poss_position_List) == 0:
        if self.current_poistion_v02 in self.past_positions_v02:
            index = self.past_positions_v02.index(self.current_poistion_v02)
            result = self.past_positions_v02[index - 1]
            self.path_return_v02.append(result)
        else:
            result = self.past_positions_v02[-1]
    if len(poss_position_List) == 1:
        result = poss_position_List[0]
    self.next_position_v02 = result