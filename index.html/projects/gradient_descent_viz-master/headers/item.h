#ifndef ITEM_H
#define ITEM_H

#include <QtDataVisualization/QCustom3DItem>
#include <QtDataVisualization/Q3DSurface>

#include "point.h"

using namespace QtDataVisualization;

// for 1 unit of magnitude, the rendered item spans this many units on the graph
// one might want to change this if gradient arrows rendered in 1:1 ratio is too
// big / small to see.
const float kItemScale = 1;
// how many items fits in one side of the graph
// don't change these. These are based on object size given in the mesh files
const float kUnitItemPerGraph = 110; // for arrows and squares
const float kBallRadiusPerGraph = 24.63;
const float kLineHalfWidth = 1. / 200.;
const float kLineLayerHeight = 0.003;
const float kLineStepSize = 1. / 50.;


class Item : public QCustom3DItem{
public:
    Item(Q3DSurface* graph) : m_graph(graph){
        m_graph->addCustomItem(this);
    }
    ~Item(){m_graph->releaseCustomItem(this);}

protected:
    Item(){}
    Q3DSurface* m_graph = nullptr;

    void setColor(QColor color);
    void addToGraph(Q3DSurface* graph);
    QVector3D plotScalingVector();
};


class Ball : public Item
{
public:
    // _f: function that defines the 3d surface the ball rolls on
    Ball(Q3DSurface* graph, QColor color, double (*_f) (double, double));
    void setPositionOnSurface(Point p);

protected:
    double (*f) (double, double);
};


class Arrow : public Item{
public:
    Arrow(Q3DSurface* graph);
    Arrow(Q3DSurface* graph, QVector3D vector);
    Arrow(Q3DSurface* graph, QVector3D vector, QColor color);
    void setVector(QVector3D vector);
    void setMagnitude(const float &magnitude);

    QVector3D renderedVectorInPlotUnit(){
        /* the xyz coordinates of the rendered vector (starts from the origin)
         * scale down by a constant because when rendering, we don't draw it
         * to the full scale (otherwise it would dominate the screen)
         */
         return direction * m_magnitude * kItemScale;
    }
    float magnitude(){return m_magnitude;}

private:
    QVector3D direction = QVector3D(0, 1, 0);
    float m_magnitude = 1.0;
};

class Square : public Item{
public:
    Square(Q3DSurface* graph);
    Square(Q3DSurface* graph, QString direction);
    void setArea(const float &area);
    // if sign is negative, flip the square 180 degree
    // (presumably to align with the gradient)
    void setArea(const float &area, const bool &is_positive);
    float area(){return m_area;}

private:
    float m_area;
    float m_is_x_direction = false;
    float m_is_positive = false;

    void flipDirection();
};


class Line : public QSurface3DSeries{
public:
   Line(Q3DSurface* graph, QColor color, double (*_f) (double, double));
   void addPoint(Point p);
   void render();
   void erase();
   void setVisible(bool visible);
   // hack: render the lines with slightly different y offsets
   // so the colors don't mix
   static int layer;

private:
   Q3DSurface* m_graph = nullptr;
   QSurfaceDataProxy* line_proxy = nullptr;
   double (*f) (double, double);
   bool m_visible = true;
   int this_layer = 0;
   bool need_to_replace_last_row = false;
   float x_range;
   float y_range;
   float z_range;
   // the cross section of a line. The line, which is really a ribbon
   // is drawn by connecting these little crosslines (left connect left,
   // right connect right)
   struct CrossLine{
       Point center;
       Point left;
       Point right;
       CrossLine(Point p) :center(p), left(p), right(p){}
   };
   std::vector<CrossLine> crosslines;

   // make data array for all point in points
   QSurfaceDataArray* getDataArray();
   QSurfaceDataRow* getDataRow(int idx);
   // if no index is specified, return the last row by default
   QSurfaceDataRow* getDataRow();
};

#endif // ITEM_H
