import cv2
import numpy as np

image_path = 'task1_image.jpg'
num_sides_list =  [3,4, 6]

image = cv2.imread(image_path)

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

find_edge = cv2.Canny(image, 30, 200)

contours, hierarchy = cv2.findContours(find_edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

triangles = []
hexagons = []

for contour in contours:
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) in num_sides_list:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            if len(approx) == 3:  # Triangle
                triangles.append((cx, cy))
            elif len(approx) == 6:  # Hexagon
                hexagons.append((cx, cy))
            # elif len(approx) == 4:  # square
            #     squares.append((cx, cy))
            cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)
            if len(approx) == 3:  # Triangle
                cv2.putText(image, 'centroid', (cx - 30, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(image, 'Triangle', (cx - 30, cy + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            elif len(approx) == 6:  # Hexagon
                cv2.putText(image, 'centroid', (cx - 30, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(image, 'Hexagon', (cx - 30, cy + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            # elif len(approx) == 4:  # square
            #     cv2.putText(image, 'centroid', (cx - 30, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #     cv2.putText(image, 'square', (cx - 30, cy + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
squares = []

if len(contours) > 0:
    moments = cv2.moments(contours[0])
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # square
            squares.append((cx, cy))

    cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)
    cv2.putText(image, 'centroid', (cx - 30, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(image, 'square', (cx - 30, cy + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 5)
    
triangles = list(set(triangles))
hexagons = list(set(hexagons))
squares = list(set(squares))

with open('TASK1_output.txt', 'w') as file:
    file.write("Triangle centroids:\n")
    for centroid in triangles:
        file.write(f"Triangle: {centroid}\n")

    file.write("square centroids:\n")
    for centroid in squares:
        file.write(f"square: {centroid}\n")
    
    file.write("Hexagon centroids:\n")
    for centroid in hexagons:
        file.write(f"Hexagon: {centroid}\n")
    
cv2.imshow('RESULT', image)
cv2.waitKey(0)
cv2.destroyAllWindows()