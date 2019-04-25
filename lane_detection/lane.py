import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 100)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]

    polygons = np.array([
        [(0, height), (width, height), (int(width/2), int(height*3/5))]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)

    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)

    # draw lines
    if lines is not None:
        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 3)

    return line_image

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    width = image.shape[1]

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if abs(slope) > 3/10:
                if slope < 0:
                    left_fit.append((slope, intercept))
                else:
                    right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        left_line = make_coordinates(image, left_fit_average)
        right_line = make_coordinates(image, right_fit_average)

        return np.array([left_line, right_line])

    else:
        return np.array([None, None])


def make_coordinates(image, line_parameters):
    try:
        _ = iter(line_parameters)

        slope, intercept = line_parameters
        y1 = image.shape[0]
        y2 = int(y1*(4/5))
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return np.array([x1, y1, x2, y2])
    except TypeError as e:
        return None

def warp(image):
    width, height = image.shape[1], image.shape[0]

    src = np.float32([
        [10, height],
        [140, height],
        [110, 140],
        [48, 140]
    ])
    dst = np.float32([
        [width/5, height],
        [width*4/5, height],
        [width*4/5, 0],
        [width/5, 0]
    ])

    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)

    warped = cv2.warpPerspective(image, M, (width, height), flags=cv2.INTER_LINEAR)
    return warped,M,Minv

#binary image
def color_mask(color_space,low,high):
    mask = cv2.inRange(color_space, low, high)
    return mask

# apply color to the binary image
def apply_color_mask(color_space,img,low,high):
    mask = cv2.inRange(color_space, low, high)
    result = cv2.bitwise_and(img,img, mask= mask)
    return result

def detect_lines(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    white_lines = color_mask(image_gray, 200, 255) # EV3
    blurred_lines = cv2.GaussianBlur(white_lines, (5, 5), 0)
    return blurred_lines

def moving_average(image, n=3):
    # Moving average
    ret = np.cumsum(image, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def initial_mask(image, window_size):
    img_size=(image.shape[1], image.shape[0])
    mov_filtsize = int(img_size[1]/50.)
    mean_lane = np.mean(image[:,:],axis=0)
    mean_lane = moving_average(mean_lane)

    # find peak indice from histogram (indice is sorted)
    indice = find_peaks_cwt(mean_lane,[30],max_distances=[176])

    val_ind = np.array([mean_lane[indice[i]] for i in range(len(indice)) ])
    ind_sorted = np.argsort(-val_ind)

    if len(ind_sorted) > 0:
        ind_peakR = indice[ind_sorted[0]]
        if len(ind_sorted) > 1:
            ind_peakL = indice[ind_sorted[1]]
        else:
            ind_peakL = 0
    else:
        ind_peakR = 0
        ind_peakL = 0

    # exchange indice if under condition
    if ind_peakR<ind_peakL:
        ind_peakR,ind_peakL = ind_peakL,ind_peakR

    # take windows from each index
    ind_min_L = ind_peakL-window_size
    ind_max_L = ind_peakL+window_size

    ind_min_R = ind_peakR-window_size
    ind_max_R = ind_peakR+window_size

    mask_L = np.zeros_like(image)
    mask_R = np.zeros_like(image)

    ind_peakR_prev = ind_peakR
    ind_peakL_prev = ind_peakL

    # Split image into 11 parts and compute histogram on each part
    for i in range(11):
        img_y1 = int(img_size[1]-img_size[1]*i/11)
        img_y2 = int(img_size[1]-img_size[1]*(i+1)/11)

        mean_lane_y = np.mean(image[img_y2:img_y1,:],axis=0)
        mean_lane_y = moving_average(mean_lane_y,mov_filtsize)
        indice = find_peaks_cwt(mean_lane_y,[30], max_distances=[176])

        # if the indice are more than 2 (both side peak L,R)
        if len(indice)>1.5:
            val_ind = np.array([mean_lane[indice[i]] for i in range(len(indice)) ])
            ind_sorted = np.argsort(-val_ind)

            ind_peakR = indice[ind_sorted[0]]
            ind_peakL = indice[ind_sorted[1]]
            if ind_peakR<ind_peakL:
                ind_peakR,ind_peakL = ind_peakL,ind_peakR

        else:
        # if one peak is found
            if len(indice)==1:
                #found right lane
                if (np.abs(indice[0]-ind_peakR_prev)<np.abs(indice[0]-ind_peakL_prev)):
                    ind_peakR = indice[0]
                    ind_peakL = ind_peakL_prev
                # found left lane
                else:
                    ind_peakL = indice[0]
                    ind_peakR = ind_peakR_prev
            # If no pixels are found, use previous ones.
            else:
                ind_peakL = ind_peakL_prev
                ind_peakR = ind_peakR_prev


        # If new center is more than 80pixels away, use previous
        # Outlier rejection
        if np.abs(ind_peakL-ind_peakL_prev)>=80:
            ind_peakL = ind_peakL_prev

        if np.abs(ind_peakR-ind_peakR_prev)>=80:
            ind_peakR = ind_peakR_prev



        mask_L[img_y2:img_y1,ind_peakL-window_size:ind_peakL+window_size] = 1.
        mask_R[img_y2:img_y1,ind_peakR-window_size:ind_peakR+window_size] = 1.

        ind_peakL_prev = ind_peakL
        ind_peakR_prev = ind_peakR

    return mask_L,mask_R

# function for polynomial fit
def polyfit(line,thresh=0.5,lane_range=[5,90],side='left'):
    img_size = (line.shape[1],line.shape[0])
    vals = np.argwhere(line > thresh)

    if not (line == np.zeros_like(line)).all():
        all_x = vals.T[0]
        all_y = vals.T[1]
        small,large = np.percentile(all_y,lane_range)
        all_y = all_y[np.where((all_y>=small) & (all_y<=large))]
        all_x = all_x[np.where((all_y>=small) & (all_y<=large))]
        fit = np.polyfit(all_x, all_y, 2)

        y = np.arange(11)*img_size[1]/10
        fitx = fit[0] * y**2 + fit[1]*y + fit[2]

    else:
        y = np.arange(11)*img_size[1]/10
        fitx = np.zeros(y.shape)
        if side != 'left':
            fitx[:] = img_size[0]-1

    return fitx, y

def slope(pts):
    x1, y1 = pts[0][0][0], pts[0][0][1]
    x2, y2 = pts[0][-1][0], pts[0][-1][1]
    slope = (y1-y2)/(x1-x2)
    return slope


def simple_lane(image_name):
    image = cv2.imread(image_name)
    lane_image = np.copy(image)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 20, np.array([]), minLineLength=3, maxLineGap=2)
    averaged_lines = average_slope_intercept(lane_image, lines)
    line_image = display_lines(lane_image, averaged_lines)
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1.0, 1.0)
    cv2.imshow('result', combo_image)
    cv2.waitKey(0)
    # plt.imshow(combo_image)
    # plt.show()

def advanced_lane(image_name):
    image = cv2.imread(image_name)
    lane_image = np.copy(image)
    warped, M, Minv = warp(lane_image)
    white_lines = detect_lines(warped)
    # mean_lane = moving_average(white_lines)
    mask_L, mask_R = initial_mask(white_lines, window_size=5)

    wpb_zero = np.zeros_like(white_lines).astype(np.uint8)
    color_warp = np.dstack((wpb_zero, wpb_zero, wpb_zero))

    left_fitx , left_y = polyfit(mask_L,thresh=0.5,lane_range=[5,95],side='left')
    right_fitx, right_y = polyfit(mask_R,thresh=0.5,lane_range=[5,95],side='right')
    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, left_y]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, right_y])))])

    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

    newwarp = cv2.warpPerspective(color_warp, Minv, (lane_image.shape[1], lane_image.shape[0]))
    result = cv2.addWeighted(lane_image, 1, newwarp, 0.3, 0)

    cv2.imshow('result', result)
    cv2.waitKey(0)

    # plt.subplot(1,2,1)
    # plt.imshow(mask_L,cmap='gray')
    # plt.axis('off')
    # plt.title('Left lane')
    # plt.subplot(1,2,2)
    # plt.imshow(mask_R,cmap='gray')
    # plt.axis('off')
    # plt.title('Right lane')
    # plt.show()

if __name__ == '__main__':
    simple_lane('test1.jpg')
    # advanced_lane('test1.jpg')
