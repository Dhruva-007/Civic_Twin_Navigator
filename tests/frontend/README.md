# Frontend Tests

Frontend testing is handled through:

1. **Manual testing** - All pages tested manually during development
2. **Backend API tests** - Full API coverage in `tests/backend/`
3. **Future** - Component tests with Vitest can be added here

## Pages Tested Manually
- Home (Login, Signup, ForgotPassword)
- Dashboard (Journey, Steps, Scores)
- MissionMode (Missions, Scenarios)
- ReadinessReport (Scores, Proof)

## Run Backend Tests
```bash
cd tests/backend
pytest -v --tb=short