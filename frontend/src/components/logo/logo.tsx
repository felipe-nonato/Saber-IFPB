import React from "react";
import "./logo.css";

export default function Logo() {
    return (
        <div className="logo-container">
            <div className="icon">
                <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <path
                        className="book"
                        d="M 50 100 C 30 90, 20 120, 50 150 L 150 150 C 180 120, 170 90, 150 100 Z"
                        stroke="#3730A3"
                        strokeWidth="5"
                    />
                    <path
                        className="book"
                        d="M 50 100 C 60 95, 70 90, 100 90 C 130 90, 140 95, 150 100 Z"
                        stroke="#3730A3"
                        strokeWidth="5"
                    />

                    <path
                        className="pages"
                        d="M 55 105 C 40 98, 30 125, 55 145 L 95 145 L 95 105 Z"
                    />
                    <path
                        className="pages"
                        d="M 145 105 C 160 98, 170 125, 145 145 L 105 145 L 105 105 Z"
                    />

                    <g className="lightbulb">
                        <circle cx="100" cy="70" r="30" />
                        <rect
                            x="90"
                            y="95"
                            width="20"
                            height="15"
                            rx="5"
                            ry="5"
                        />
                        <rect
                            x="94"
                            y="107"
                            width="12"
                            height="5"
                            rx="2"
                            ry="2"
                        />
                    </g>

                    <g className="data-points">
                        <circle cx="70" cy="60" r="4" />
                        <circle cx="130" cy="60" r="4" />
                        <circle cx="80" cy="40" r="4" />
                        <circle cx="120" cy="40" r="4" />
                    </g>
                </svg>
            </div>
            <h1 className="text-4xl font-bold text-gray-800 mt-4">SABER</h1>
            <p className="text-center text-gray-600 mt-2">
                Sistema de Análise de Bibliografias e Estudos Recomendados
            </p>
        </div>
    );
}
