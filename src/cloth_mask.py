import cv2
import os
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def bfs_black(x, y, a, mask):
    mask[x][y] = 0
    queue = [(x, y)]

    while len(queue):
        current_x, current_y = queue[len(queue) - 1]
        queue.pop()

        for i in range(4):
            nx = dx[i] + current_x
            ny = dy[i] + current_y

            if nx < 0 or ny < 0 or nx >= len(a) or ny >= len(a[0]) or mask[nx][ny] == 0 or a[nx][ny] < 246:
                continue

            mask[nx][ny] = 0
            queue.append((nx, ny))

    return mask

def bfs_white(x, y, a, mask):
    mask[x][y] = 255
    queue = [(x, y)]

    while len(queue):
        current_x, current_y = queue[len(queue) - 1]
        queue.pop()

        for i in range(4):
            nx = dx[i] + current_x
            ny = dy[i] + current_y

            if nx < 0 or ny < 0 or nx >= len(a) or ny >= len(a[0]) or mask[nx][ny] == 255 or a[nx][ny] == 0:
                continue

            mask[nx][ny] = 255
            queue.append((nx, ny))

    return mask

def create_mask(image):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mask = gray_image.copy()
    for x in range(0, len(mask)):
        for y in range(0, len(mask[x])):
            mask[x][y] = 255
    bfs_black(0, 0, gray_image, mask)

    mask2 = mask.copy()
    for x in range(0, len(mask2)):
        for y in range(0, len(mask2[x])):
            mask2[x][y] = 0
    bfs_white(len(mask2) // 2, len(mask2[0]) // 2, mask, mask2)
    
    return cv2.medianBlur(mask2, 5)

def main():
    for filename in os.listdir("image"):

        image = cv2.imread(os.path.join("image", filename))

        mask = create_mask(image)
        print('complete masking ' + filename)

        cv2.imwrite(os.path.join("mask", filename[:-4] + "_mask.jpg"), mask)

main()