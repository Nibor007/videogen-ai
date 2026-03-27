import pytest
from unittest.mock import patch, MagicMock
from graph.state import VideoState

def make_state(**kwargs) -> VideoState:
    base = VideoState(
        prompt="test prompt",
        job_id="test-123",
        script=None,
        audio_url=None,
        images=None,
        video_url=None,
        errors=[],
        retry_count=0,
        status="pending"
    )
    base.update(kwargs)
    return base

# Tests agente de guión
class TestScriptAgent:
    @patch("agents.script_agent.ChatAnthropic")
    def test_script_generado_correctamente(self, mock_llm):
        from agents.script_agent import script_agent
        
        mock_response = MagicMock()
        mock_response.content = '{"titulo":"Test","escenas":[{"numero":1,"narracion":"texto","descripcion_visual":"imagen","duracion_seg":5}]}'
        mock_llm.return_value.invoke.return_value = mock_response
        
        state = make_state()
        result = script_agent(state)
        
        assert result["status"] == "script_done"
        assert result["script"]["titulo"] == "Test"
        assert len(result["script"]["escenas"]) == 1
        assert result["errors"] == []

    @patch("agents.script_agent.ChatAnthropic")
    def test_script_error_incrementa_retry(self, mock_llm):
        from agents.script_agent import script_agent
        
        mock_llm.return_value.invoke.side_effect = Exception("API error")
        
        state = make_state()
        result = script_agent(state)
        
        assert result["retry_count"] == 1
        assert len(result["errors"]) == 1
        assert "script" in result["errors"][0]

# Tests agente de audio mock
class TestAudioAgent:
    def test_audio_mock_exitoso(self):
        from agents.audio_agent import audio_agent
        
        state = make_state(
            script={"titulo":"Test","escenas":[{"narracion":"texto de prueba"}]}
        )
        result = audio_agent(state)
        
        assert result["status"] == "audio_done"
        assert result["audio_url"] is not None
        assert "s3://" in result["audio_url"]
        assert result["errors"] == []

# Tests agente de imágenes mock
class TestImagesAgent:
    def test_images_mock_exitoso(self):
        from agents.images_agent import images_agent
        
        state = make_state(
            script={"titulo":"Test","escenas":[
                {"numero":1,"descripcion_visual":"imagen 1"},
                {"numero":2,"descripcion_visual":"imagen 2"}
            ]}
        )
        result = images_agent(state)
        
        assert result["status"] == "images_done"
        assert len(result["images"]) == 2
        assert result["errors"] == []

# Tests agente de video mock
class TestVideoAgent:
    def test_video_mock_exitoso(self):
        from agents.video_agent import video_agent
        
        state = make_state(
            script={"titulo":"Test","escenas":[]},
            audio_url="s3://bucket/audio.mp3",
            images=["s3://bucket/img1.jpg"]
        )
        result = video_agent(state)
        
        assert result["status"] == "done"
        assert result["video_url"] is not None
        assert result["errors"] == []

# Tests de condiciones del grafo
class TestConditions:
    def test_after_script_sin_errores(self):
        from graph.conditions import after_script
        state = make_state(errors=[])
        assert after_script(state) == "next"

    def test_after_script_con_errores(self):
        from graph.conditions import after_script
        state = make_state(errors=["script: error"])
        assert after_script(state) == "retry"

    def test_after_video_sin_errores(self):
        from graph.conditions import after_video
        state = make_state(errors=[])
        assert after_video(state) == "end"

    def test_after_video_con_errores(self):
        from graph.conditions import after_video
        state = make_state(errors=["video: error"])
        assert after_video(state) == "retry"