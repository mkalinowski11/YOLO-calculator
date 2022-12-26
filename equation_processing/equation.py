import numpy as np

class Equation:
  def __init__(self, idx, prediction):
    self.eq_coord = prediction[idx]
    self.elements = self.__get_elements(prediction, idx)
  
  def __get_elements(self, prediction, eq_idx):
    results = []
    for idx, entry in enumerate(prediction):
      if idx != eq_idx:
        bbox_intersect = self.intersect(entry, prediction[eq_idx, :])
        if bbox_intersect >= 0.5:
          results.append(entry)
    results  = self.__remove_doubles(results)
    results = self.sort_items(results)
    return results
  
  def __call__(self):
    return self.elements
  
  def __len__(self):
    return len(self.elements)
  
  def __remove_doubles(self, elements):
    boxes = []
    for box in elements:
      intersection = 0
      for element in boxes:
        new_intersection = self.intersect(element, box)
        intersection = max(intersection, new_intersection)
      if intersection < 0.5:
        boxes.append(box)
    return boxes

  def __calculate_area(self, bbox):
    x = abs(bbox[3] - bbox[1])
    y = abs(bbox[4] - bbox[2])
    return x * y

  def intersect(self, box1, box2):
      x1 = max(box1[1], box2[1])
      y1 = max(box1[2], box2[2])
      x2 = min(box1[3], box2[3])
      y2 = min(box1[4], box2[4])
      intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
      area1 = self.__calculate_area(box1)
      area2 = self.__calculate_area(box2)
      area1_factor = intersection / area1
      area2_factor = intersection / area2
      area_factor = max(area1_factor, area2_factor)
      return area_factor
  
  def sort_items(self, elements):
    sorted_items = sorted(elements, key = lambda entry : entry[1])
    return np.array(sorted_items)