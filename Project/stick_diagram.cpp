#include "stick_diagram.h"
#include <algorithm>
#include <cmath>

StickDiagram::StickDiagram(QWidget *parent) : QWidget(parent) {}

void StickDiagram::setData(const std::vector<std::string>& eulerPathNmos,
                          const std::vector<std::string>& eulerPathPmos,
                          const std::vector<std::string>& sourceNodesPmos,
                          const std::vector<std::string>& sourceNodesNmos,
                          const std::vector<std::string>& outNodesPmos,
                          const std::vector<std::string>& outNodesNmos,
                          const std::vector<std::string>& logicElements) {
    this->eulerPathNmos = eulerPathNmos;
    this->eulerPathPmos = eulerPathPmos;
    this->sourceNodesPmos = sourceNodesPmos;
    this->sourceNodesNmos = sourceNodesNmos;
    this->outNodesPmos = outNodesPmos;
    this->outNodesNmos = outNodesNmos;
    this->logicElements = logicElements;
    
    // Calculate coordinates
    for (size_t i = 0; i < eulerPathPmos.size(); i++) {
        double x = 100 + i * 30;
        coordinatesPmos[eulerPathPmos[i]] = std::make_pair(x, 200);
    }
    
    for (size_t i = 0; i < eulerPathNmos.size(); i++) {
        double x = 100 + i * 30;
        coordinatesNmos[eulerPathNmos[i]] = std::make_pair(x, 400);
    }
    
    update();
}

void StickDiagram::paintEvent(QPaintEvent *event) {
    Q_UNUSED(event);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Set background
    painter.fillRect(rect(), Qt::white);
    
    drawVddGnd(painter);
    drawLogicElements(painter);
    drawPmosNetwork(painter);
    drawNmosNetwork(painter);
    drawVddConnections(painter);
    drawGndConnections(painter);
    drawOutputConnections(painter);
}

void StickDiagram::drawVddGnd(QPainter &painter) {
    // Draw Vdd line
    painter.setPen(QPen(Qt::blue, 2));
    painter.drawLine(50, 150, 500, 150);
    painter.drawText(510, 150, "Vdd");
    
    // Draw Gnd line
    painter.drawLine(50, 450, 500, 450);
    painter.drawText(510, 450, "Gnd");
    
    // Draw power rails
    painter.setPen(QPen(Qt::yellow, 2));
    painter.drawLine(50, 180, 500, 180);
    
    painter.setPen(QPen(Qt::green, 2));
    painter.drawLine(50, 420, 500, 420);
}

void StickDiagram::drawLogicElements(QPainter &painter) {
    painter.setPen(QPen(Qt::red, 1));
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);
    
    for (size_t i = 0; i < logicElements.size(); i++) {
        double x = 150 + i * 60;
        painter.drawLine(x, 170, x, 430);
        painter.drawText(x, 165, QString::fromStdString(logicElements[i]));
    }
}

void StickDiagram::drawPmosNetwork(QPainter &painter) {
    painter.setPen(QPen(Qt::black, 1));
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);
    
    // Draw PMOS labels
    for (const auto& pmos : eulerPathPmos) {
        auto coord = coordinatesPmos[pmos];
        painter.drawText(coord.first, coord.second - 10, QString::fromStdString(pmos));
    }
    
    // Draw PMOS connections (simplified)
    for (size_t i = 1; i < eulerPathPmos.size(); i++) {
        auto prev = coordinatesPmos[eulerPathPmos[i-1]];
        auto curr = coordinatesPmos[eulerPathPmos[i]];
        
        if (std::abs(curr.first - prev.first) > 30) {
            painter.drawLine(prev.first, prev.second, prev.first, prev.second - 20);
            painter.drawLine(curr.first, curr.second, curr.first, curr.second - 20);
            painter.drawLine(prev.first, prev.second - 20, curr.first, curr.second - 20);
            
            painter.drawEllipse(QPointF(prev.first, prev.second), 3, 3);
            painter.drawEllipse(QPointF(curr.first, curr.second), 3, 3);
        }
    }
}

void StickDiagram::drawNmosNetwork(QPainter &painter) {
    painter.setPen(QPen(Qt::black, 1));
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);
    
    // Draw NMOS labels
    for (const auto& nmos : eulerPathNmos) {
        auto coord = coordinatesNmos[nmos];
        painter.drawText(coord.first, coord.second + 20, QString::fromStdString(nmos));
    }
    
    // Draw NMOS connections (simplified)
    for (size_t i = 1; i < eulerPathNmos.size(); i++) {
        auto prev = coordinatesNmos[eulerPathNmos[i-1]];
        auto curr = coordinatesNmos[eulerPathNmos[i]];
        
        if (std::abs(curr.first - prev.first) > 30) {
            painter.drawLine(prev.first, prev.second, prev.first, prev.second + 20);
            painter.drawLine(curr.first, curr.second, curr.first, curr.second + 20);
            painter.drawLine(prev.first, prev.second + 20, curr.first, curr.second + 20);
            
            painter.drawEllipse(QPointF(prev.first, prev.second), 3, 3);
            painter.drawEllipse(QPointF(curr.first, curr.second), 3, 3);
        }
    }
}

void StickDiagram::drawVddConnections(QPainter &painter) {
    painter.setPen(QPen(Qt::blue, 1));
    
    for (const auto& node : sourceNodesPmos) {
        auto coord = coordinatesPmos[node];
        painter.drawLine(coord.first, coord.second, coord.first, 180);
        painter.drawLine(coord.first, 180, coord.first, 150);
        painter.drawEllipse(QPointF(coord.first, coord.second), 3, 3);
    }
}

void StickDiagram::drawGndConnections(QPainter &painter) {
    painter.setPen(QPen(Qt::blue, 1));
    
    for (const auto& node : sourceNodesNmos) {
        auto coord = coordinatesNmos[node];
        painter.drawLine(coord.first, coord.second, coord.first, 420);
        painter.drawLine(coord.first, 420, coord.first, 450);
        painter.drawEllipse(QPointF(coord.first, coord.second), 3, 3);
    }
}

void StickDiagram::drawOutputConnections(QPainter &painter) {
    painter.setPen(QPen(Qt::red, 1));
    QFont font = painter.font();
    font.setPointSize(12);
    painter.setFont(font);
    
    // Draw output label
    painter.drawText(450, 300, "Y");
    
    // Connect PMOS output
    for (const auto& node : outNodesPmos) {
        auto coord = coordinatesPmos[node];
        painter.drawLine(coord.first, coord.second, coord.first, coord.second + 50);
        painter.drawLine(coord.first, coord.second + 50, 450, 300);
    }
    
    // Connect NMOS output
    for (const auto& node : outNodesNmos) {
        auto coord = coordinatesNmos[node];
        painter.drawLine(coord.first, coord.second, coord.first, coord.second - 50);
        painter.drawLine(coord.first, coord.second - 50, 450, 300);
    }
}
