from scene import *
import ui
import random
import numpy as np
import speech
import time


def gradient_descent_line_fitter(x, y, learning_rate = 0.02, stop_criteria = 1e-4, max_iter = 10000):
  scaling_factor = 100.0
  x = x/scaling_factor
  y = y/scaling_factor
  
  def partial_derivative_b(a, b, x, y):
    return np.mean(2 * a * x + 2 * b - 2 * y)

  def partial_derivative_a(a, b, x, y):
    return np.mean((2 * a * x + 2 * b - 2 * y) * x)

  a = 0
  b = 0
  
  for i in xrange(max_iter):
    old_a = a
    old_b = b

    a += -learning_rate * partial_derivative_a(old_a, old_b, x, y)
    b += -learning_rate * partial_derivative_b(old_a, old_b, x, y)
  
    if i % 100 == 0 and i != 0:
      print 'a = ' + str(a) + ', b = ' + str(b*scaling_factor)
      line_path = ui.Path()
      line_path.move_to(0,0)
      line_path.line_to(-1024, a*1024)
      line_path.line_width = 2
      test_line = ShapeNode(path=line_path, fill_color='white', stroke_color='white')
      test_line.position = (512,b*scaling_factor + a*512)
      if view.scene.line:
        view.scene.line.remove_from_parent()
      view.scene.add_child(test_line)
      view.scene.line = test_line
      speech.say('jumped ' + str(i) + ' times', 'en-US')
      time.sleep(1)
    
    if abs(a - old_a) < stop_criteria and abs(b - old_b) < stop_criteria:
      break

  return (a, b*scaling_factor)

# print gradient_descent_line_fitter(x, y)
# print a, b

points = []

class MyScene (Scene):
  def setup(self):
    self.background_color = 'midnightblue'
    self.point_size = 5
    bg_text = LabelNode('Gradient Descent Optimization', font=('Helvetica', 60))
    bg_text.position =self.size / 2
    bg_text.color = (.5, .5, .5)
    self.add_child(bg_text)
    self.line = None

  def touch_began(self, touch):
    x, y = touch.location
    #generate 100 points near touch location
    for i in range(100):
      dist = random.uniform(0, 100)
      angle = random.uniform(0, 2*math.pi)
      rand_x = x + dist*math.cos(angle)
      rand_y = y + dist*math.sin(angle)
      points.append((rand_x, rand_y))
      
      this_point = ShapeNode(path=ui.Path.oval(0, 0, self.point_size, self.point_size), fill_color=(1,1,1), stroke_color='clear')
      this_point.position = (rand_x , rand_y)
      self.add_child(this_point)
    

@ui.in_background
def button_tapped(sender):
  if len(points) <= 0:
    print('gimme points')
    return
  x = []
  y = []
  for point in points:
    x.append(point[0])
    y.append(point[1])
  np_x = np.array(x, dtype = np.float64)
  np_y = np.array(y, dtype = np.float64)
  (a, b) = gradient_descent_line_fitter(np_x, np_y)
  print 'a = ' + str(a) + ', b = ' + str(b)
  line_path = ui.Path()
  line_path.move_to(0,0)
  line_path.line_to(-1024, a*1024)
  line_path.line_width = 3
  test_line = ShapeNode(path=line_path, fill_color='red', stroke_color='red')
  test_line.position = (512,b + a*512)
  view.scene.add_child(test_line)
  speech.say('I am done!')


view = SceneView()
view.scene = MyScene()
button = ui.Button(title = 'Find Line of Best Fit')
button.font = ('Chalkboard SE', 30)
button.tint_color = (.0, .0, .0)
button.background_color = (.72, .67, 1.0)
button.corner_radius = 5
button.border_width = 1
button.border_color = (1, 1, 1)
button.width = 300
button.x = 350
button.y = 720
button.action = button_tapped

view.add_subview(button)
view.present()
