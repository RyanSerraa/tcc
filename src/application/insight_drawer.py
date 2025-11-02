import json

import plotly.graph_objects as go

from src.domain.state import State


class InsightDrawer:
    def __init__(self, agent):
        self.insight_drawer = agent

    def respond(self, state: State):
        refazer_grafico = state.redator_response.get("redoChart")
        base_prompt = f'Pergunta: "{state.question}".\nDados: "{state.result}".\n'
        if refazer_grafico:
            base_prompt += f"Refazer gráfico: {state.chartEditor_response}\n"
        response = self.insight_drawer.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": base_prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        response_json = json.loads(content)
        return {"chartEditor_response": response_json}

    @staticmethod
    def mountChart(graph_json):
        chart_type = graph_json.get("type", "bar").lower()
        layout = graph_json.get("layout", {})
        data = graph_json.get("data", [])
        fig = None

        if chart_type in ["bar"]:
            fig = go.Figure()
            for series in data:
                fig.add_trace(
                    go.Bar(
                        x=series["x"],
                        y=series["y"],
                        name=series.get("name", ""),
                        marker=series.get("marker", {}),
                    )
                )
            if layout.get("barmode"):
                fig.update_layout(barmode=layout.get("barmode"))
        elif chart_type in ["line"]:
            fig = go.Figure()
            for series in data:
                fig.add_trace(
                    go.Scatter(
                        x=series["x"],
                        y=series["y"],
                        mode="lines+markers",
                        name=series.get("name", ""),
                        line=series.get("line", {}),
                        marker=series.get("marker", {}),
                    )
                )
        elif chart_type in ["scatter"]:
            fig = go.Figure()
            for series in data:
                fig.add_trace(
                    go.Scatter(
                        x=series["x"],
                        y=series["y"],
                        mode="markers",
                        name=series.get("name", ""),
                        marker=series.get("marker", {}),
                    )
                )
        elif chart_type in ["pie"]:
            series = data[0] if data else {}
            fig = go.Figure(
                go.Pie(
                    labels=series.get("x", []),
                    values=series.get("y", []),
                    name=series.get("name", ""),
                    marker=series.get("marker", {}),
                )
            )
        if fig is not None:
            fig.update_layout(
                title=layout.get("title", ""),
                xaxis_title=(
                    layout.get("xaxis", {}).get("title", "")
                    if chart_type not in ["pie"]
                    else None
                ),
                yaxis_title=(
                    layout.get("yaxis", {}).get("title", "")
                    if chart_type not in ["pie"]
                    else None
                ),
                legend=layout.get("legend", {}),
            )
        return fig
