import { useState } from "react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"

// Sample page: one of each building block on the theme. Replace it with the real app.
export function App() {
  const [name, setName] = useState("")
  const invalid = name.length > 0 && name.trim().length < 2

  return (
    <main className="mx-auto flex min-h-svh max-w-3xl flex-col gap-8 p-6">
      <header className="flex flex-col gap-1">
        <p className="text-label text-muted-foreground">sample</p>
        <h1 className="text-3xl font-semibold">Sample page</h1>
        <p className="text-muted-foreground">
          本文は sans、見出しは heading、
          <span className="text-keyword">keyword</span> は nav、
          <code>code</code> は mono。 日本語はどれも同じ字形に落ちる。
        </p>
      </header>

      <section className="flex flex-col gap-3">
        <h2 className="text-xl font-semibold">Buttons</h2>
        <div className="flex flex-wrap gap-2">
          <Button>Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="link">Link</Button>
          <Button disabled>Disabled</Button>
        </div>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Form</CardTitle>
          <CardDescription>
            Inputs, select and toggles on a card.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="flex flex-col gap-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              placeholder="at least 2 characters"
              value={name}
              onChange={(e) => setName(e.target.value)}
              aria-invalid={invalid}
            />
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <Select defaultValue="day">
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="day">Day</SelectItem>
                <SelectItem value="week">Week</SelectItem>
                <SelectItem value="month">Month</SelectItem>
              </SelectContent>
            </Select>
            <ToggleGroup defaultValue={["list"]} variant="outline">
              <ToggleGroupItem value="list">List</ToggleGroupItem>
              <ToggleGroupItem value="grid">Grid</ToggleGroupItem>
            </ToggleGroup>
            <Badge>badge</Badge>
            <Badge variant="secondary">secondary</Badge>
          </div>
        </CardContent>
        <CardFooter className="gap-2">
          <Button disabled={invalid || name.length === 0}>Save</Button>
          <Button variant="ghost">Cancel</Button>
        </CardFooter>
      </Card>

      <section className="flex flex-col gap-3">
        <h2 className="text-xl font-semibold">Code</h2>
        <p>
          Inline <code>npm run check</code> and a block:
        </p>
        <pre>
          <code>{`npm run dev     # http://localhost:5173\nnpm run check   # format, lint, typecheck, build`}</code>
        </pre>
      </section>
    </main>
  )
}

export default App
