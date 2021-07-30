while true do
    local p = Instance.New("Part")
    p.Size = Vector3.New(3,3,3)
    p.Color3 = Color3.Random()
    p.Position = script.Parent.Position
    p.Anchored = false
    wait(0.1)
end