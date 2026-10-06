\# Architecture



\## Initial Architecture



The AI Interviewer Platform will initially use a modular monolith architecture.



The frontend and backend are separate applications, while backend functionality is organized into modules.



```text

Frontend

&#x20;   |

&#x20;   | HTTP / WebSocket / WebRTC

&#x20;   |

Backend

&#x20;   |

&#x20;   +-- Authentication

&#x20;   +-- Candidate Management

&#x20;   +-- Interview Management

&#x20;   +-- Resume / JD Analysis

&#x20;   +-- AI Interview Engine

&#x20;   +-- Evaluation

&#x20;   +-- Consistency Analysis

&#x20;   +-- Monitoring

&#x20;   |

&#x20;   +-- PostgreSQL

&#x20;   +-- AI Services

&#x20;   +-- Storage

