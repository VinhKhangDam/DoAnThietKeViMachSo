#ifndef STICK_DIAGRAM_H
#define STICK_DIAGRAM_H

#include <QWidget>
#include <QPainter>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <utility>

class StickDiagram : public QWidget {
    Q_OBJECT
public:
    explicit StickDiagram(QWidget *parent = nullptr);
    void setData(const std::vector<std::string>& eulerPathNmos,
                const std::vector<std::string>& eulerPathPmos,
                const std::vector<std::string>& sourceNodesPmos,
                const std::vector<std::string>& sourceNodesNmos,
                const std::vector<std::string>& outNodesPmos,
                const std::vector<std::string>& outNodesNmos,
                const std::vector<std::string>& logicElements);

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    std::vector<std::string> eulerPathNmos;
    std::vector<std::string> eulerPathPmos;
    std::vector<std::string> sourceNodesPmos;
    std::vector<std::string> sourceNodesNmos;
    std::vector<std::string> outNodesPmos;
    std::vector<std::string> outNodesNmos;
    std::vector<std::string> logicElements;
    
    std::map<std::string, std::pair<double, double>> coordinatesPmos;
    std::map<std::string, std::pair<double, double>> coordinatesNmos;
    std::set<std::pair<double, double>> connectedPmos;
    std::set<std::pair<double, double>> connectedNmos;
    
    void drawVddGnd(QPainter &painter);
    void drawLogicElements(QPainter &painter);
    void drawPmosNetwork(QPainter &painter);
    void drawNmosNetwork(QPainter &painter);
    void drawVddConnections(QPainter &painter);
    void drawGndConnections(QPainter &painter);
    void drawOutputConnections(QPainter &painter);
};

#endif // STICK_DIAGRAM_H
